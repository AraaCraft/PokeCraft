import re
import json

def parse_fr():
    with open("scratch/fr_megas.html", "r") as f:
        html = f.read()
    matches = re.findall(r'<td.*?>\s*<img.*?src="([^"]+)".*?>\s*</td>\s*<td.*?>([^<]+)</td>', html)
    return [(img.strip(), name.strip()) for img, name in matches]

fr_megas = parse_fr()

# Manual mapping FR -> EN based on my knowledge of Pokemon FR/EN names
fr_to_en_map = {
    "Florizarrite": "Venusaurite",
    "Dracaufite X": "Charizardite X",
    "Dracaufite Y": "Charizardite Y",
    "Tortankite": "Blastoisinite",
    "Dardargnite": "Beedrillite",
    "Roucarnagite": "Pidgeotite",
    "Raichuïte X": "Raichunite X",
    "Raichuïte Y": "Raichunite Y",
    "Mélodelfite": "Clefablite",
    "Alakazamite": "Alakazite",
    "Empiflorite": "Victreebelite",
    "Flagadossite": "Slowbronite",
    "Ectoplasmite": "Gengarite",
    "Kangourexite": "Kangaskhanite",
    "Starossite": "Starminite",
    "Scarabruite": "Pinsirite",
    "Léviatorite": "Gyaradosite",
    "Ptéraïte": "Aerodactylite",
    "Dracolossite": "Dragoninite",
    "Méganiumite": "Meganiumite",
    "Aligatueurite": "Feraligite",
    "Pharampite": "Ampharosite",
    "Steelixite": "Steelixite",
    "Cizayoxite": "Scizorite",
    "Scarhinoïte": "Heracronite",
    "Airmurite": "Skarmorite",
    "Démolossite": "Houndoominite",
    "Tyranocivite": "Tyranitarite",
    "Jungkite": "Sceptilite",
    "Braségalite": "Blazikenite",
    "Laggronite": "Swampertite",
    "Gardevoirite": "Gardevoirite",
    "Ténéfixite": "Sablenite",
    "Galekingite": "Aggronite",
    "Mysdibulite": "Mawilite",
    "Charminite": "Medichamite",
    "Élecsprintite": "Manectite",
    "Sharpedite": "Sharpedonite",
    "Caméruptite": "Cameruptite",
    "Altarite": "Altarianite",
    "Branettite": "Banettite",
    "Éokite": "Chimechite",
    "Absolite": "Absolite",
    "Oniglalite": "Glalitite",
    "Métalossite": "Metagrossite",
    "Lockpinite": "Lopunnite",
    "Carchacrokite": "Garchompite",
    "Étouraptorite": "Staraptite",
    "Lucarite": "Lucarionite",
    "Blizzarite": "Abomasite",
    "Gallamite": "Galladite",
    "Momartikite": "Froslassite",
    "Roitiflamite": "Emboarite",
    "Minotaupite": "Excadrite",
    "Nanméouïte": "Audinite",
    "Brutapodite": "Scolipite",
    "Baggaïdite": "Scraftinite",
    "Lugulabrite": "Chandelurite",
    "Ohmassacrite": "Eelektrossite",
    "Golemastokite": "Golurkite",
    "Blindépiquite": "Chesnaughtite",
    "Goupelinite": "Delphoxite",
    "Amphinolite": "Greninjite",
    "Floettite": "Floettite",
    "Mistigrixite": "Meowsticite",
    "Néméliosite": "Pyroarite",
    "Sépiatrocite": "Malamarite",
    "Golgopathite": "Barbaracite",
    "Brutalibrite": "Hawluchanite",
    "Kravarekite": "Dragalgite",
    "Crabominablite": "Crabominite",
    "Draïeulite": "Drampanite",
    "Hexadronite": "Falinksite",
    "Scovilainite": "Scovillainite",
    "Floréclatite": "Glimmoranite"
}

with open("frontend/public/data/items.json", "r") as f:
    items = json.load(f)

# We want to remove ALL items in the current json that look like mega stones
# and replace them with exactly this list.
new_items = {}
generic_sprite = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/mega-bracelet.png"

for k, v in items.items():
    name = v.get("name", "")
    is_mega_stone = False
    if name.endswith("ite") or name.endswith("ite-x") or name.endswith("ite-y") or name.endswith("ite-z"):
        if name not in ["eviolite", "white", "meteorite", "lite", "polite"]:
            is_mega_stone = True
            
    if not is_mega_stone:
        new_items[k] = v

max_id = max([int(k) for k in new_items.keys()] + [10000])

for img, name_fr in fr_megas:
    name_en = fr_to_en_map.get(name_fr, name_fr + "ite")
    # internal name
    name_id = name_en.lower().replace(" ", "-").replace("ï", "i").replace("é", "e")
    
    max_id += 1
    
    new_items[str(max_id)] = {
        "id": max_id,
        "name": name_id,
        "name_en": name_en,
        "name_fr": name_fr,
        "effect_en": "Allows a certain Pokémon to Mega Evolve in battle.",
        "effect_fr": "Permet à un certain Pokémon de méga-évoluer en combat.",
        "sprite": img if img else generic_sprite
    }

with open("frontend/public/data/items.json", "w") as f:
    json.dump(new_items, f, indent=2)

print("Merged properly. The list is now EXACTLY what Pokekalos provided.")
