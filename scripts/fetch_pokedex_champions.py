# 26/06/2026
# Version : 1.0
# Descrtiption : Script pour récupérer les données des pokémons présent sur Pokémon Champions

import requests
import json
import os

# S'assure que le dossier data existe
os.makedirs('data', exist_ok=True)

pokemon = {
    "id":None,
    "name":None,
    "form":None,
    "abilities":None,
    "stats":None,
    "types":None,
    "weight":None,
}
champions_dex_url_api = "https://pokeapi.co/api/v2/pokedex/36/"
# entries est une liste de tous les pokémon de champions
entries = requests.get(champions_dex_url_api).json()["pokemon_entries"]

# On itère pour chaque pokémon dans la liste
for entry in entries:
    print(entry["entry_number"], entry["pokemon_species"]["name"],
          entry["pokemon_species"]["url"])
    # On crée le dossier pour le pokémon en question
    pokemon_dir = f"data/champions/pokemon/{entry["entry_number"]}"
    os.makedirs(pokemon_dir, exist_ok=True)
    # varieties est une liste des formes du pokémon en question
    varieties = requests.get(entry["pokemon_species"]["url"]).json()["varieties"]

    for variety in varieties:
        # variety_data est le json de la forme en question
        variety_data = requests.get(variety["pokemon"]["url"]).json()
        pokemon["id"] = entry["entry_number"]
        pokemon["name"] = entry["pokemon_species"]["name"]
        pokemon["form"] = variety["pokemon"]["name"]
        pokemon["abilities"] = variety_data["abilities"]
        pokemon["stats"] = variety_data["stats"]
        pokemon["types"] = variety_data["types"]
        pokemon["weight"] = variety_data["weight"]
        # Si le lien pour récupérer le cri du pokémon en question existe
        if (variety_data["cries"]["latest"]):
            cry_raw = requests.get(variety_data["cries"]["latest"])
            # On crée le fichier .ogg du cri du pokémon en question dans le dossier pokemon_dir/
            open(f"{pokemon_dir}/{variety["pokemon"]["name"]}.ogg", 'wb').write(cry_raw.content)
        # Si le lien pour récupérer le sprite de face du pokémon en question existe
        if (variety_data["sprites"]["front_default"]):
            front_sprite_default_raw = requests.get(variety_data["sprites"]["front_default"])
            open(f"{pokemon_dir}/{variety["pokemon"]["name"]}-front_default.png", 'wb').write(front_sprite_default_raw.content)
        front_sprite_female_raw = None      # Plus tard
        # Si le lien pour récupérer le sprite de dos du pokémon en question existe
        if (variety_data["sprites"]["back_default"]):
            back_sprite_default_raw = requests.get(variety_data["sprites"]["back_default"])
            open(f"{pokemon_dir}/{variety["pokemon"]["name"]}-back_default.png", 'wb').write(back_sprite_default_raw.content)
        back_sprite_female_raw = None       # Plus tard

        # Génère le json du pokémon en question, par forme, indent=4 pour plus de lisibilité
        json_str = json.dumps(pokemon, indent=4)
        # On crée le fichier json du pokémon en question, par forme, dans le dossier pokemon_dir/ dans un dossier avec son id pokédex
        with open(f"{pokemon_dir}/{variety["pokemon"]["name"]}.json", "w") as f:
            f.write(json_str)
