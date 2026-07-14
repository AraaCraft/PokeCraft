import os
import json
import glob

base_dir = "data/champions/pokemon"
mega_forms = []

for filepath in glob.glob(f"{base_dir}/*/*.json"):
    with open(filepath, 'r') as f:
        data = json.load(f)
        form = data.get("form", "")
        if "-mega" in form:
            mega_forms.append(form)

print("Mega Forms found:", sorted(mega_forms))
