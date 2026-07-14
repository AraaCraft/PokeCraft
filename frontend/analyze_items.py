import json

with open('public/data/items.json', 'r') as f:
    items = json.load(f)

print("Total items:", len(items))

no_sprite = sum(1 for v in items.values() if not v.get('sprite'))
no_effect = sum(1 for v in items.values() if not v.get('effect_en'))

print("No sprite:", no_sprite)
print("No effect:", no_effect)

# sample no sprite
print("Sample no sprite:", [v['name_en'] for v in items.values() if not v.get('sprite')][:10])
print("Sample no effect:", [v['name_en'] for v in items.values() if not v.get('effect_en')][:10])

categories = {'berries': 0, 'mega': 0, 'other': 0}
for v in items.values():
    name = v.get('name_en', '').lower()
    if 'berry' in name:
        categories['berries'] += 1
    elif 'ite' in name or 'ite ' in name or name.endswith('ite'):
        categories['mega'] += 1
    else:
        categories['other'] += 1

print("Categories count:", categories)
