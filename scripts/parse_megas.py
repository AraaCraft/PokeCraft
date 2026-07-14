import re

def parse_fr():
    with open("scratch/fr_megas.html", "r") as f:
        html = f.read()
    
    # <td style="min-width: 50px;"><img src="https://www.media.pokekalos.fr/img/pokemon/objets/big/florizarrite.png" width="30px"></td><td style="min-width: 50px;">Florizarrite</td>
    matches = re.findall(r'<td.*?>\s*<img.*?src="([^"]+)".*?>\s*</td>\s*<td.*?>([^<]+)</td>', html)
    return matches

def parse_en():
    with open("scratch/en_megas.html", "r") as f:
        html = f.read()
    
    # game8 usually uses a table with <tr><td><a><img>...</a></td><td>Name</td>
    # or something similar. Let's try a very loose match for images and text in adjacent cells.
    # We can also just extract all rows.
    # For now let's just see if we can find words like 'ite' in the HTML.
    megas = set(re.findall(r'>([a-zA-Z\s\-]+ite\s*[XY]?)<', html, re.IGNORECASE))
    return list(megas)

print("FR Megas:")
fr_megas = parse_fr()
for img, name in fr_megas:
    print(f" - {name} ({img})")

print("\nEN Megas (guess):")
en_megas = parse_en()
for name in en_megas:
    print(f" - {name}")

