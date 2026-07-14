import json
import glob

items = []
for filepath in glob.glob("data/items/*.json"):
    with open(filepath, 'r') as f:
        data = json.load(f)
        name = data.get("name", "")
        # A simple heuristic for mega stones
        if name.endswith("ite") or name.endswith("ite-x") or name.endswith("ite-y") or name.endswith("ite-z"):
            if name not in ["eviolite", "white", "meteorite"]:
                items.append(name)

print("Mega items found:", sorted(items))
