import json

x = '{"name" : "Bek" , "age" : 30, "city" : "Bishkek"}'

y = json.loads(x)
print(y["name"])