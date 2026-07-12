import json
import glob
import os
import urllib.request

pokemon_files = glob.glob('data/champions/pokemon/**/*.json', recursive=True)

# Group files by ID
by_id = {}
for f in pokemon_files:
    with open(f, 'r') as file:
        data = json.load(file)
        pid = data['id']
        if pid not in by_id:
            by_id[pid] = []
        by_id[pid].append((f, data))

def get_base_form(forms):
    # Find the one where name == form
    for f, d in forms:
        if d['name'] == d['form']:
            return f, d
    # Or shortest name
    return min(forms, key=lambda x: len(x[1]['form']))

updates = 0

for pid, forms in by_id.items():
    base_file, base_data = get_base_form(forms)
    
    # If base form has 0 moves, try fetching from pokeapi
    if len(base_data.get('moves', [])) == 0:
        print(f"Fetching moves for base form {base_data['name']} (ID: {pid}) from PokeAPI...")
        try:
            req = urllib.request.Request(f"https://pokeapi.co/api/v2/pokemon/{pid}", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    pokeapi_data = json.loads(response.read().decode())
                    moves = []
                    for m in pokeapi_data.get('moves', []):
                        # extract move ID from URL
                        url = m['move']['url']
                        move_id = int(url.strip('/').split('/')[-1])
                        moves.append(move_id)
                    if moves:
                        base_data['moves'] = moves
                        with open(base_file, 'w') as out:
                            json.dump(base_data, out, indent=4)
                        print(f"-> Saved {len(moves)} moves to {base_file}")
                        updates += 1
        except Exception as e:
            print(f"Error fetching for {pid}: {e}")

    # Now base_data might have moves. Update any forms that have 0 moves.
    base_moves = base_data.get('moves', [])
    if len(base_moves) > 0:
        for f, d in forms:
            if len(d.get('moves', [])) == 0:
                d['moves'] = base_moves
                with open(f, 'w') as out:
                    json.dump(d, out, indent=4)
                print(f"-> Copied {len(base_moves)} moves from base to {f}")
                updates += 1

print(f"Finished fixing moves. Files updated: {updates}")
