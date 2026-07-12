import json
import os
import urllib.request
import urllib.error

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    print("Fetching natures from PokeAPI...")
    
    # PokeAPI has 25 natures
    data = fetch_json("https://pokeapi.co/api/v2/nature?limit=50")
    if not data or 'results' not in data:
        print("Failed to fetch natures list.")
        return

    natures_data = {}
    
    neutral_natures = ["hardy", "docile", "bashful", "quirky", "serious"]
    
    for item in data['results']:
        name = item['name']
        
        # Filter neutral natures, keep only serious
        if name in neutral_natures and name != "serious":
            continue
            
        nature_detail = fetch_json(item['url'])
        if not nature_detail:
            continue
            
        nature_id = str(nature_detail['id'])
        
        # Extract names (en and fr)
        name_en = name.capitalize()
        name_fr = name.capitalize()
        for n in nature_detail.get('names', []):
            if n['language']['name'] == 'en':
                name_en = n['name']
            elif n['language']['name'] == 'fr':
                name_fr = n['name']
                
        increased = nature_detail.get('increased_stat')
        decreased = nature_detail.get('decreased_stat')
        
        inc_stat = increased['name'] if increased else None
        dec_stat = decreased['name'] if decreased else None
        
        natures_data[nature_id] = {
            "id": nature_id,
            "name": name,
            "name_en": name_en,
            "name_fr": name_fr,
            "increased_stat": inc_stat,
            "decreased_stat": dec_stat
        }
        print(f"Processed {name_en} (+{inc_stat}, -{dec_stat})")

    # Export to JSON
    os.makedirs('frontend/public/data', exist_ok=True)
    out_path = 'frontend/public/data/natures.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(natures_data, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {out_path} with {len(natures_data)} natures.")

if __name__ == "__main__":
    main()
