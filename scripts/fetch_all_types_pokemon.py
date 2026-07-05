# 05/07/2026
# Version : 1.0
# Descrtiption : Script pour récupérer tous les types (types) existants dans les jeux Pokémons

import requests
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "..", "data", "types")
os.makedirs(output_dir, exist_ok=True)

list_types_url = "https://pokeapi.co/api/v2/type/"
print(f"Fetching types list from {list_types_url}...")
types_response = requests.get(list_types_url).json()
types = types_response["results"]

print(f"Found {len(types)} types. Fetching details...")

for type_entry in types:
    try:
        type_details = requests.get(type_entry["url"]).json()

        # PokeAPI returns some dummy types like "unknown" or "shadow", we keep them just in case, but they usually don't matter much.
        type_name = type_details["name"]

        data_to_save = {
            "id": type_details["id"],
            "name": type_name,
            "damage_relations": type_details["damage_relations"]
        }

        # On sauvegarde dans /data/types/
        json_str = json.dumps(data_to_save, indent=4, ensure_ascii=False)
        with open(os.path.join(output_dir, f"{type_name}.json"), "w", encoding="utf-8") as f:
            f.write(json_str)

        print(f"✅ Saved type: {type_name}")

    except Exception as e:
        print(f"❌ Error fetching {type_entry['name']}: {e}")

print("🎉 Tous les types ont été téléchargés !")
