import json

with open("man.json", "r") as file:
    data = json.load(file)

print(data)