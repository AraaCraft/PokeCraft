import os
import json
import glob

base_dir = "data/champions/pokemon"
mega_pokemons = []

for filepath in glob.glob(f"{base_dir}/*/*.json"):
    with open(filepath, 'r') as f:
        data = json.load(f)
        if "-mega" in data.get("form", ""):
            mega_pokemons.append(data.get("name"))

mega_pokemons = list(set(mega_pokemons))
print("Mega Pokemons found:", sorted(mega_pokemons))
