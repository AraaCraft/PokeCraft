import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor

frontend_file = "/Users/margauxbrun/PokeCraft/frontend/public/data/abilities.json"
data_dir = "/Users/margauxbrun/PokeCraft/data/abilities"

with open(frontend_file, 'r', encoding='utf-8') as f:
    frontend_data = json.load(f)

def fetch_and_patch(key):
    ability = frontend_data[key]
    ability_id = ability["id"]
    url = f"https://pokeapi.co/api/v2/ability/{ability_id}/"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            
            desc_en = None
            desc_fr = None
            
            for entry in data.get("effect_entries", []):
                if entry.get("language", {}).get("name") == "en":
                    desc_en = entry.get("effect") or entry.get("short_effect")
                if entry.get("language", {}).get("name") == "fr":
                    desc_fr = entry.get("effect") or entry.get("short_effect")
            
            if desc_en:
                ability["description_en"] = desc_en.replace("\n", " ").replace("\f", " ")
            if desc_fr:
                ability["description_fr"] = desc_fr.replace("\n", " ").replace("\f", " ")
                
            # Update individual file in data/abilities if it exists
            indiv_file = os.path.join(data_dir, f"{ability_id}.json")
            if os.path.exists(indiv_file):
                with open(indiv_file, 'r', encoding='utf-8') as f:
                    indiv_data = json.load(f)
                indiv_data["description_en"] = ability["description_en"]
                indiv_data["description_fr"] = ability["description_fr"]
                with open(indiv_file, 'w', encoding='utf-8') as f:
                    json.dump(indiv_data, f, indent=4, ensure_ascii=False)
            
            print(f"Patched ability {ability_id} ({key})")
    except Exception as e:
        print(f"Failed to patch ability {ability_id}: {e}")

if __name__ == "__main__":
    keys = list(frontend_data.keys())
    print(f"Found {len(keys)} abilities to patch...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(fetch_and_patch, keys)
        
    with open(frontend_file, 'w', encoding='utf-8') as f:
        json.dump(frontend_data, f, indent=4, ensure_ascii=False)
    print("Done patching abilities")
