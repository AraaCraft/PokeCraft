import os
import json
import glob
import requests
from concurrent.futures import ThreadPoolExecutor

output_dir = "/Users/margauxbrun/PokeCraft/data/moves"

def fetch_and_patch(filepath):
    move_id = os.path.basename(filepath).replace(".json", "")
    url = f"https://pokeapi.co/api/v2/move/{move_id}/"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            with open(filepath, 'r', encoding='utf-8') as f:
                move_data = json.load(f)
            
            desc_en = None
            desc_fr = None
            
            # Extraire les effect_entries (short_effect ou effect)
            for entry in data.get("effect_entries", []):
                if entry.get("language", {}).get("name") == "en":
                    desc_en = entry.get("short_effect") or entry.get("effect")
                if entry.get("language", {}).get("name") == "fr":
                    desc_fr = entry.get("short_effect") or entry.get("effect")
            
            # S'il n'y a pas d'effect_entries (très rare, mais possible), on garde le flavor text actuel
            if desc_en:
                move_data["description_en"] = desc_en.replace("\n", " ")
            if desc_fr:
                move_data["description_fr"] = desc_fr.replace("\n", " ")
                
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(move_data, f, indent=4, ensure_ascii=False)
            
            print(f"Patched move {move_id}")
    except Exception as e:
        print(f"Failed to patch move {move_id}: {e}")

if __name__ == "__main__":
    files = glob.glob(os.path.join(output_dir, "*.json"))
    print(f"Found {len(files)} moves to patch...")
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(fetch_and_patch, files)
    print("Done patching moves")
