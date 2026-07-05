# 05/07/2026
# Version : 1.0
# Descrtiption : Script pour récupérer tous les talents (abilities) existants dans les jeux Pokémons

import requests
import json
import os

ability_to_register = {
    "id": None,
    "name": None,
    "name_fr": None,
    "name_en": None,
    "description_fr": None,
    "description_en": None,
}

# Pour que le script fonctionne aussi bien en local sur Mac que dans Docker, on calcule le chemin relatif
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "..", "data", "abilities")
os.makedirs(output_dir, exist_ok=True)

list_abilities_url = "https://pokeapi.co/api/v2/ability/?limit=1000"
print(f"Fetching abilities list from {list_abilities_url}...")
abilities_response = requests.get(list_abilities_url).json()
abilities = abilities_response["results"]

print(f"Found {len(abilities)} abilities. Fetching details...")

for ability in abilities:
    try:
        ability_details = requests.get(ability["url"]).json()

        # On passe les talents qui n'ont pas d'ID valide (ex: certains talents custom de la PokeAPI s'ils existent)
        if "id" not in ability_details:
            continue

        ability_to_register["id"] = ability_details["id"]
        ability_to_register["name"] = ability_details["name"]

        # Récupération des noms localisés
        ability_to_register["name_fr"] = None
        ability_to_register["name_en"] = None
        for name_entry in ability_details.get("names", []):
            if name_entry["language"]["name"] == "fr":
                ability_to_register["name_fr"] = name_entry["name"]
            if name_entry["language"]["name"] == "en":
                ability_to_register["name_en"] = name_entry["name"]

        # Fallback si pas de nom en/fr
        if not ability_to_register["name_en"]:
            ability_to_register["name_en"] = ability_details["name"].replace("-", " ").title()
        if not ability_to_register["name_fr"]:
            ability_to_register["name_fr"] = ability_to_register["name_en"]

        # Récupération des descriptions (flavor_text)
        ability_to_register["description_fr"] = None
        ability_to_register["description_en"] = None

        for flavor_entry in ability_details.get("flavor_text_entries", []):
            # On prend la première description trouvée pour la langue
            if flavor_entry["language"]["name"] == "fr" and not ability_to_register["description_fr"]:
                ability_to_register["description_fr"] = flavor_entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')
            if flavor_entry["language"]["name"] == "en" and not ability_to_register["description_en"]:
                ability_to_register["description_en"] = flavor_entry["flavor_text"].replace('\n', ' ').replace('\f', ' ')

        # On sauvegarde dans /app/data/abilities/
        json_str = json.dumps(ability_to_register, indent=4, ensure_ascii=False)
        with open(f"{output_dir}/{ability_to_register['id']}.json", "w", encoding="utf-8") as f:
            f.write(json_str)

        print(f"✅ Saved ability: {ability_to_register['name']} (ID: {ability_to_register['id']})")

        # Reset pour le prochain itération
        ability_to_register = {
            "id": None,
            "name": None,
            "name_fr": None,
            "name_en": None,
            "description_fr": None,
            "description_en": None,
        }
    except Exception as e:
        print(f"❌ Error fetching {ability['name']}: {e}")

print("🎉 Toutes les capacités ont été téléchargées !")
