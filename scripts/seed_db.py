import os
import json
from flask import Flask
from db_model import db, Pokemon, Move

# On recrée une instance Flask juste pour ce script
app = Flask(__name__)
# N'oublie pas de mettre la bonne URL de connexion MySQL de ton docker-compose
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://champions_user:champions_pwd@db/champions_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def load_moves_from_json():
    # Chemin vers ton dossier d'attaques
    moves_dir = 'data/moves/'
    if not os.path.exists(moves_dir):
        print(f"Le dossier {moves_dir} n'existe pas.")
        return

    print("Chargement des attaques...")
    for filename in os.listdir(moves_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(moves_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # Création de l'objet Move (adapte les clés selon ton JSON)
                new_move = Move(
                    id=data.get('id'),
                    name=data.get('name'),
                    type=data.get('type'),
                    power=data.get('power'),
                    accuracy=data.get('accuracy')
                )
                db.session.merge(new_move) # merge = insert ou update si l'ID existe déjà

    db.session.commit()
    print("✅ Attaques chargées en base !")

def load_pokemon_from_json():
    # Chemin vers le dossier Pokémon
    pokemon_dir = '/app/data/champions/pokemon/'
    if not os.path.exists(pokemon_dir):
        print(f"Le dossier {pokemon_dir} n'existe pas.")
        return

    print("Chargement des Pokémon...")
    for filename in os.listdir(pokemon_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(pokemon_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # Adapte ces clés en fonction de la structure exacte de TES fichiers JSON
                stats = data.get('stats', {})
                new_pokemon = Pokemon(
                    id=data.get('id'),
                    name=data.get('name'),
                    hp=stats.get('hp'),
                    attack=stats.get('attack'),
                    defense=stats.get('defense'),
                    sp_attack=stats.get('special-attack'),
                    sp_defense=stats.get('special-defense'),
                    speed=stats.get('speed'),
                    types=",".join(data.get('types', [])),
                    sprite_url=data.get('sprite')
                )
                db.session.merge(new_pokemon)

    db.session.commit()
    print("✅ Pokémon chargés en base !")

if __name__ == '__main__':
    # Flask a besoin d'un "contexte d'application" pour parler à la base de données
    with app.app_context():
        # Optionnel: ça crée les tables dans MySQL si elles n'existent pas encore
        db.create_all()

        # On lance nos fonctions de lecture
        load_moves_from_json()
        load_pokemon_from_json()
        print("🎉 Base de données initialisée avec succès depuis tes fichiers locaux !")
