import re
import json

with open("scratch/en_megas.html", "r") as f:
    html = f.read()

# Let's just find anything matching /alt=['"]([^'"]+ite[ XZ]*)['"]/i
matches = re.findall(r"alt=['\"]([^'\"]+ite[ XZ]*)['\"]", html, re.IGNORECASE)
for m in set(matches):
    if m.lower() not in ["white", "meteorite", "eviolite", "other items"]:
        print(m.strip())
