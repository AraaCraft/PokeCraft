import json
import glob
import os

with open('data/excluded_forms.json', 'r') as f:
    EXCLUDED_FORMS = json.load(f)

pokemon_files = glob.glob('data/champions/pokemon/**/*.json', recursive=True)
search_index = {}

for f in pokemon_files:
    with open(f, 'r') as file:
        data = json.load(file)
        if '-gmax' in data['form']: continue
        if data['form'] in EXCLUDED_FORMS: continue
        if data['id'] == 25 and data['form'] != 'pikachu': continue
        
        pid = data['id']
        name = data['name'].capitalize()
        name_fr = data.get('name_fr', name).capitalize()
        name_en = data.get('name_en', name).capitalize()
        if pid not in search_index:
            search_index[pid] = {
                'id': pid,
                'name': name_en,
                'name_fr': name_fr,
                'name_en': name_en,
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
