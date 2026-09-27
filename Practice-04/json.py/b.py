import json

person = {
    "name": "Jeff",
    "age": 70,
    "student": False
}

data = json.dumps(person)

print(data)