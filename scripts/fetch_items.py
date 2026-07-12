import json
import os
import urllib.request
import re
import html
from concurrent.futures import ThreadPoolExecutor, as_completed

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
POKEBIP_URL = "https://www.pokebip.com/page/jeux-video/pokemon-champions/liste-objets-tenus"

def get_champions_item_names():
    req = urllib.request.Request(POKEBIP_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8')
        
        matches = re.findall(r'<strong>.*?</strong><br><em>(.*?)</em>', html_content)
        names = []
        for m in matches:
            decoded = html.unescape(m)
            # transform to pokeapi id
            name = decoded.lower().replace(' ', '-').replace("'", '').replace('.', '').replace('é', 'e')
            names.append(name)
        return names
    except Exception as e:
        print(f"Error fetching from Pokebip: {e}")
        return []

def fetch_item_details(item_name):
    url = f"{POKEAPI_BASE_URL}/item/{item_name}/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if not data:
            return None
        
        name_en = item_name.replace('-', ' ').title()
        name_fr = name_en
        
        for name_obj in data.get('names', []):
            if name_obj['language']['name'] == 'en':
                name_en = name_obj['name']
            if name_obj['language']['name'] == 'fr':
                name_fr = name_obj['name']
                
        effect_en = ""
        effect_fr = ""
        
        # Try effect_entries first (user specifically requested 'effect' over 'short_effect')
        for entry in data.get('effect_entries', []):
            if entry['language']['name'] == 'en':
                effect_en = entry.get('effect') or entry.get('short_effect', '')
                effect_en = effect_en.replace('\n', ' ')
            if entry['language']['name'] == 'fr':
                effect_fr = entry.get('effect') or entry.get('short_effect', '')
                effect_fr = effect_fr.replace('\n', ' ')
                
        # Fallback to flavor_text_entries if empty
        if not effect_en:
            for entry in data.get('flavor_text_entries', []):
                if entry['language']['name'] == 'en':
                    effect_en = entry['text'].replace('\n', ' ')
                if entry['language']['name'] == 'fr':
                    effect_fr = entry['text'].replace('\n', ' ')
                
        if not effect_fr:
            effect_fr = effect_en

        return {
            "id": data["id"],
            "name": item_name,
            "name_en": name_en,
            "name_fr": name_fr,
            "effect_en": effect_en,
            "effect_fr": effect_fr,
            "sprite": data.get("sprites", {}).get("default", "")
        }
    except Exception as e:
        print(f"Error fetching details for {item_name}: {e}")
        return None

def get_mega_stones():
    url = f"{POKEAPI_BASE_URL}/item-category/44/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        return [item['name'] for item in data['items']]
    except Exception as e:
        print(f"Error fetching mega stones: {e}")
        return []

def main():
    print("Fetching items list from Pokebip...")
    item_names = get_champions_item_names()
    
    print("Fetching mega stones list from PokeAPI...")
    mega_stones = get_mega_stones()
    
    item_names = list(set(item_names + mega_stones))
    
    if not item_names:
        print("Failed to retrieve items.")
        return

    print(f"Found {len(item_names)} items. Fetching details from PokeAPI...")
    
    items_map = {}
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(fetch_item_details, name): name for name in item_names}
        for future in as_completed(futures):
            res = future.result()
            if res:
                items_map[str(res["id"])] = res
            
    output_dir = "frontend/public/data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "items.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(items_map, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(items_map)} items to {output_path}")

if __name__ == "__main__":
    main()
