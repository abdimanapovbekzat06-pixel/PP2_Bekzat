import json

man = {
    "name": "Benjamin",
    "age": 76,
    "height": 178
}

with open("man.json", "w") as file:
    json.dump(man, file, indent = 4)