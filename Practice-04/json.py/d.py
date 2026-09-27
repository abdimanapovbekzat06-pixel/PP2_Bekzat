import json

with open("man.json", "r") as file:
    man = json.load(file)

print(man)

