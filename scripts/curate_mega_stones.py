import json
import glob

# 1. Collect all mega forms
base_dir = "data/champions/pokemon"
mega_forms = []

for filepath in glob.glob(f"{base_dir}/*/*.json"):
    with open(filepath, 'r') as f:
        data = json.load(f)
        form = data.get("form", "")
        if "-mega" in form:
            name_en = data.get("name_en", "")
            name_fr = data.get("name_fr", "")
            mega_forms.append({
                "form": form,
                "base_id": data.get("id"),
                "base_name": data.get("name"),
                "name_en": name_en,
                "name_fr": name_fr
            })

# Hardcoded known stone mappings (base_name -> stone_name)
stone_map = {
    "abomasnow": "abomasite",
    "aerodactyl": "aerodactylite",
    "houndoom": "houndoominite",
    "manectric": "manectite",
    "medicham": "medichamite",
    "camerupt": "cameruptite",
    "banette": "banettite",
    "tyranitar": "tyranitarite",
    "blastoise": "blastoisinite",
    "venusaur": "venusaurite",
    "kangaskhan": "kangaskhanite",
    "pinsir": "pinsirite",
    "gyarados": "gyaradosite",
    "ampharos": "ampharosite",
    "scizor": "scizorite",
    "heracross": "heracronite",
    "alakazam": "alakazite",
    "gengar": "gengarite",
    "pidgeot": "pidgeotite",
    "slowbro": "slowbronite",
    "steelix": "steelixite",
    "sceptile": "sceptilite",
    "swampert": "swampertite",
    "sableye": "sablenite",
    "sharpedo": "sharpedonite",
    "glalie": "glalitite",
    "salamence": "salamencite",
    "metagross": "metagrossite",
    "lopunny": "lopunnite",
    "garchomp": "garchompite",
    "lucario": "lucarionite",
    "gallade": "galladite",
    "audino": "audinite",
    "charizard": ["charizardite-x", "charizardite-y"],
    "mewtwo": ["mewtwonite-x", "mewtwonite-y"],
    
    # Customs
    "delphox": "delphoxite",
    "chesnaught": "chesnaughtite",
    "greninja": "greninjite",
    "crabominable": "crabominite",
    "dragalge": "dragalgite",
    "drampa": "drampanite",
    "eelektross": "eelektrossite",
    "emboar": "emboarite",
    "excadrill": "excadrite",
    "falinks": "falinksite",
    "feraligatr": "feraligite",
    "floette": "floettite",
    "froslass": "froslassite",
    "glimmora": "glimmoranite",
    "golurk": "golurkite",
    "hawlucha": "hawluchanite",
    "malamar": "malamarite",
    "mawile": "mawilite",
    "meganium": "meganiumite",
    "meowstic": "meowsticite",
    "pyroar": "pyroarite",
    "raichu": ["raichunite-x", "raichunite-y"],
    "scolipede": "scolipite",
    "scovillain": "scovillainite",
    "scrafty": "scraftinite",
    "staraptor": "staraptite",
    "starmie": "starminite",
    "victreebel": "victreebelite",
    "barbaracle": "barbaracite",
    "chandelure": "chandelurite",
    "clefable": "clefablite",
    "dragonite": "dragoninite",
    "altaria": "altarianite",
    "absol": ["absolite", "absolite-z"]
}

# Add garchomp-z and lucario-z
stone_map["garchomp"] = ["garchompite", "garchompite-z"]
stone_map["lucario"] = ["lucarionite", "lucarionite-z"]

valid_stone_names = set()
for mf in mega_forms:
    base = mf["base_name"]
    stones = stone_map.get(base)
    if not stones:
        # fallback guess
        stones = base + "ite"
    
    if isinstance(stones, list):
        for s in stones:
            valid_stone_names.add(s)
    else:
        valid_stone_names.add(stones)

with open("frontend/public/data/items.json", "r") as f:
    items = json.load(f)

new_items = {}
generic_sprite = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/mega-bracelet.png"

for k, v in items.items():
    name = v.get("name", "")
    
    is_mega_stone = False
    if name.endswith("ite") or name.endswith("ite-x") or name.endswith("ite-y") or name.endswith("ite-z"):
        if name not in ["eviolite", "white", "meteorite", "lite", "polite"]:
            is_mega_stone = True
            
    if is_mega_stone:
        if name in valid_stone_names:
            # Fix effect and sprite if empty
            if not v.get("effect_en"):
                v["effect_en"] = "Allows a certain Pokémon to Mega Evolve in battle."
            if not v.get("effect_fr"):
                v["effect_fr"] = "Permet à un certain Pokémon de méga-évoluer en combat."
            if not v.get("sprite"):
                v["sprite"] = generic_sprite
            
            # Update name strings for consistency
            if "name_en" not in v or not v["name_en"]:
                v["name_en"] = name.capitalize()
            if "name_fr" not in v or not v["name_fr"]:
                v["name_fr"] = name.capitalize()
                
            new_items[k] = v
        else:
            # Skip this mega stone because it's not valid for user's champions
            pass
    else:
        # Not a mega stone, keep it
        new_items[k] = v

# Are there any valid stones MISSING from items.json?
existing_stone_names = set()
for v in new_items.values():
    existing_stone_names.add(v["name"])

max_id = max([int(k) for k in new_items.keys()] + [10000])

for needed_stone in valid_stone_names:
    if needed_stone not in existing_stone_names:
        max_id += 1
        new_items[str(max_id)] = {
            "id": max_id,
            "name": needed_stone,
            "name_en": needed_stone.capitalize(),
            "name_fr": needed_stone.capitalize(),
            "effect_en": "Allows a certain Pokémon to Mega Evolve in battle.",
            "effect_fr": "Permet à un certain Pokémon de méga-évoluer en combat.",
            "sprite": generic_sprite
        }
        print(f"Added missing stone: {needed_stone}")

with open("frontend/public/data/items.json", "w") as f:
    json.dump(new_items, f, indent=2)

print(f"Curated mega stones. Removed unused ones, added missing ones.")
