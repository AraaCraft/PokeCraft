from flask_sqlalchemy import SQLAlchemy

# On initialise l'objet SQLAlchemy qui va gérer la BDD
db = SQLAlchemy()



class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    # L'ID sera celui de PokéAPI
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # On stocke les stats de base
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    sp_attack = db.Column(db.Integer)
    sp_defense = db.Column(db.Integer)
    speed = db.Column(db.Integer)

    # Pour le type, on peut utiliser une simple chaîne (ex: "eau,vol") pour simplifier le MVP
    type_1 = db.Column(db.Integer, nullable=False)
    type_2 = db.Column(db.Integer, nullable=True)
    sprite_url = db.Column(db.String(255))

class Move(db.Model):
    __tablename__ = 'moves'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(50))
    power = db.Column(db.Integer, nullable=True) # Peut être null pour les attaques de statut
    accuracy = db.Column(db.Integer, nullable=True)

class Type(db.Model):
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Relation_Pokemon_Type(db.Model):
    __tablename__ = 'relations_pokemon_type'

    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
