import json
import urllib.request
import os

# Ensure image directory exists
img_dir = "frontend/public/images/items"
os.makedirs(img_dir, exist_ok=True)

# Load current items
with open("data/items.json", "r") as f:
    items = json.load(f)

print(f"Loaded {len(items)} items")

downloaded = 0
for k, v in items.items():
    name = v.get("name", "")
    sprite_url = v.get("sprite", "")
    
    is_mega_stone = False
    if name.endswith("ite") or name.endswith("ite-x") or name.endswith("ite-y") or name.endswith("ite-z"):
        if name not in ["eviolite", "white", "meteorite", "lite", "polite"]:
            is_mega_stone = True
            
    if is_mega_stone and sprite_url.startswith("http"):
        # We need to download this sprite
        filename = f"{name}.png"
        filepath = os.path.join(img_dir, filename)
        
        try:
            req = urllib.request.Request(sprite_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(filepath, "wb") as img_file:
                    img_file.write(response.read())
            
            # Update json to point to local path
            v["sprite"] = f"/images/items/{filename}"
            downloaded += 1
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {sprite_url} for {name}: {e}")

with open("data/items.json", "w") as f:
    json.dump(items, f, indent=2)

print(f"Successfully downloaded {downloaded} mega stone sprites and updated items.json")
