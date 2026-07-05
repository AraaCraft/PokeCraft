# 26/06/2026
# Version : 1.0
# Descrtiption : Script pour récupérer tous les moves existants dans les jeux Pokémons

import requests
import json
import os

# Set correct output directory
output_dir = "/Users/margauxbrun/PokeCraft/data/moves"
os.makedirs(output_dir, exist_ok=True)

move_to_register = {
    "accuracy":None,
    "damage_class":None,
    "description_en":None,
    "effect_chance":None,
    "effect_changes":None,
    "effect_entries":None,
    "id":None,
    "meta":{        # (sauf les url)
        "ailment_name":None,
        "ailment_chance":None,
        "category_name":None,
        "crit_rate":None,
        "drain":None,
        "flinch_chance":None,
        "healing":None,
        "max_hits": None,
        "max_turns":None,
        "min_hits":None,
        "min_turns":None,
        "stat_chance":None,
    },
    "shortname":None,
    "name_fr":None,
    "name_en":None,
    "power":None,
    "pp":None,
    "priority":None,
    "stat_changes":None,
    "target_name":None,
    "type_name":None,
} 

list_moves_url = "https://pokeapi.co/api/v2/move/?limit=1000"
# moves est une liste de tous les moves du jeu
moves = requests.get(list_moves_url).json()["results"]


# https://pokeapi.co/api/v2/move/{id}/
for move in moves:
    # print(move["name"])
    move_details = requests.get(move["url"]).json()
    move_to_register["accuracy"] = move_details["accuracy"]
    move_to_register["damage_class"] = move_details["damage_class"]["name"]
    move_to_register["effect_chance"] = move_details["effect_chance"]
    move_to_register["effect_changes"] = move_details["effect_changes"]
    move_to_register["id"] = move_details["id"]

    # move_to_register["meta"]
    if type(move_details["meta"]) == type(dict()):
        move_to_register["meta"]["ailment_name"] = move_details["meta"]["ailment"]["name"]
        move_to_register["meta"]["ailment_chance"] = move_details["meta"]["ailment_chance"]
        move_to_register["meta"]["category_name"] = move_details["meta"]["category"]["name"]
        move_to_register["meta"]["crit_rate"] = move_details["meta"]["crit_rate"]
        move_to_register["meta"]["drain"] = move_details["meta"]["drain"]
        move_to_register["meta"]["flinch_chance"] = move_details["meta"]["flinch_chance"]
        move_to_register["meta"]["healing"] = move_details["meta"]["healing"]
        move_to_register["meta"]["max_hits"] = move_details["meta"]["max_hits"]
        move_to_register["meta"]["max_turns"] = move_details["meta"]["max_turns"]
        move_to_register["meta"]["min_hits"] = move_details["meta"]["min_hits"]
        move_to_register["meta"]["min_turns"] = move_details["meta"]["min_turns"]
        move_to_register["meta"]["stat_chance"] = move_details["meta"]["stat_chance"]

    # Extract English description
    for entry in move_details.get("flavor_text_entries", []):
        if entry.get("language", {}).get("name") == "en":
            # Remove newlines and form feeds
            move_to_register["description_en"] = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            break

    move_to_register["shortname"] = move_details["name"]
    for name in move_details["names"]:
        if (name["language"]["name"] == "fr"):
            move_to_register["name_fr"] = name["name"]
        if (name["language"]["name"] == "en"):
            move_to_register["name_en"] = name["name"]
    move_to_register["power"] = move_details["power"]
    move_to_register["pp"] = move_details["pp"]
    move_to_register["priority"] = move_details["priority"]
    move_to_register["stat_changes"] = move_details["stat_changes"]
    move_to_register["target_name"] = move_details["target"]["name"]
    move_to_register["type_name"] = move_details["type"]["name"]

    # On veut les stocker dans le répertoire de sortie local
    json_str = json.dumps(move_to_register, indent=4, ensure_ascii=False)
    with open(os.path.join(output_dir, f"{move_to_register['id']}.json"), "w", encoding="utf-8") as f:
        f.write(json_str)

    move_to_register = {
        "accuracy":None,
        "damage_class":None,
        "description_en":None,
        "effect_chance":None,
        "effect_changes":None,
        "effect_entries":None,
        "id":None,
        "meta":{
            "ailment_name":None,
            "ailment_chance":None,
            "category_name":None,
            "crit_rate":None,
            "drain":None,
            "flinch_chance":None,
            "healing":None,
            "max_hits": None,
            "max_turns":None,
            "min_hits":None,
            "min_turns":None,
            "stat_chance":None,
        },
        "shortname":None,
        "name_fr":None,
        "name_en":None,
        "power":None,
        "pp":None,
        "priority":None,
        "stat_changes":None,
        "target_name":None,
        "type_name":None,
    }
