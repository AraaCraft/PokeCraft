import json

with open("frontend/public/data/items.json", "r") as f:
    items = json.load(f)

for k, v in items.items():
    name = v.get("name", "")
    if name.endswith("ite") or name.endswith("ite-x") or name.endswith("ite-y") or name.endswith("ite-z"):
        if name not in ["eviolite", "white", "meteorite", "lite", "polite"]:
            print(name)
