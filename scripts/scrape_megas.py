import re
import json

def scrape_fr():
    with open("scratch/fr_megas.html", "r") as f:
        html = f.read()
    matches = re.findall(r'<td.*?>\s*<img.*?src="([^"]+)".*?>\s*</td>\s*<td.*?>([^<]+)</td>', html)
    megas = []
    for img, name in matches:
        megas.append({
            "name_fr": name.strip(),
            "sprite": img.strip()
        })
    return megas

def scrape_en():
    with open("scratch/en_megas.html", "r") as f:
        html = f.read()
    # Looks like <img class="a-img lazy" alt="Absolite" data-src="..."
    # Sometimes it might just be src="..." if lazy loading is bypassed. Let's find both.
    matches = re.findall(r'<img[^>]*alt="([^"]+ite[ XZ]*)"[^>]*data-src="([^"]+)"', html, re.IGNORECASE)
    if not matches:
        matches = re.findall(r'<img[^>]*alt="([^"]+ite[ XZ]*)"[^>]*src="([^"]+)"', html, re.IGNORECASE)
    
    megas = []
    for name, img in set(matches):
        if "ite" in name.lower() and name.lower() not in ["white", "meteorite", "eviolite"]:
            megas.append({
                "name_en": name.strip(),
                "sprite": img.strip()
            })
    return megas

fr_list = scrape_fr()
en_list = scrape_en()

print(f"Scraped {len(fr_list)} FR stones and {len(en_list)} EN stones.")

# Now we need to match them. 
# We'll just generate the json using FR sprites since they are provided directly by Pokekalos.
items = {}
max_id = 1000

for i, fr in enumerate(fr_list):
    name_fr = fr["name_fr"]
    # Create the internal name
    name = name_fr.lower()
    name = name.replace(" ", "-").replace("ï", "i").replace("é", "e")
    
    # Try to find corresponding EN name by order if possible? 
    # Or just guess the EN name for now and we can fix it if needed. 
    # Wait, PokeAPI has EN names. If the user only gave us 2 links, they might not match 1:1 in order.
    
    items[str(max_id + i)] = {
        "id": max_id + i,
        "name": name,
        "name_en": name, # We'll try to find EN
        "name_fr": name_fr,
        "effect_en": "Allows a certain Pokémon to Mega Evolve in battle.",
        "effect_fr": "Permet à un certain Pokémon de méga-évoluer en combat.",
        "sprite": fr["sprite"]
    }

# Dump to file to verify
with open("scratch/megas_curated.json", "w") as f:
    json.dump(items, f, indent=2)

print("Saved to scratch/megas_curated.json")
