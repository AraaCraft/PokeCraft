import json
import glob
import os

pokemon_files = glob.glob('data/champions/pokemon/**/*.json', recursive=True)
search_index = {}

for f in pokemon_files:
    with open(f, 'r') as file:
        data = json.load(file)
        if '-gmax' in data['form']: continue
        if data['id'] == 25 and data['form'] != 'pikachu': continue
        
        pid = data['id']
        name = data['name'].capitalize()
        if pid not in search_index:
            search_index[pid] = {
                'id': pid,
                'name': name,
                'base_form': data['name'],
                'forms': []
            }
        
        # Add form info if it's not the base form
        if data['name'] != data['form']:
            form_name = data['form'].replace(f"{data['name']}-", "").replace("-", " ").capitalize()
            search_index[pid]['forms'].append(form_name)

# Flatten and sort
final_list = list(search_index.values())
final_list.sort(key=lambda x: x['id'])

os.makedirs('frontend/public/data', exist_ok=True)
with open('frontend/public/data/search_index.json', 'w') as out:
    json.dump(final_list, out)

print(f"Generated search index with {len(final_list)} pokemon.")
