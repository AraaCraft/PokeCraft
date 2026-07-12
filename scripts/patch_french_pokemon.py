import json
import glob
import urllib.request
import urllib.error
import time

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}")
        return None

pokemon_files = glob.glob('data/champions/pokemon/**/*.json', recursive=True)
species_cache = {}

for f in pokemon_files:
    with open(f, 'r') as file:
        data = json.load(file)
        
    if "name_fr" in data:
        continue # already patched
        
    pid = data['id']
    if pid not in species_cache:
        url = f"https://pokeapi.co/api/v2/pokemon-species/{pid}/"
        species_data = fetch_json(url)
        if species_data:
            name_fr = data['name'] # fallback
            name_en = data['name']
            for n in species_data.get('names', []):
                if n['language']['name'] == 'fr':
                    name_fr = n['name']
                if n['language']['name'] == 'en':
                    name_en = n['name']
            species_cache[pid] = {'name_fr': name_fr, 'name_en': name_en}
            time.sleep(0.1) # be nice to pokeapi
        else:
            species_cache[pid] = {'name_fr': data['name'], 'name_en': data['name']}

    data['name_fr'] = species_cache[pid]['name_fr']
    data['name_en'] = species_cache[pid]['name_en']
    
    with open(f, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
    print(f"Patched {f} with FR: {data['name_fr']}")
