names = ["Ali", "Bekzat", "Dias"]
ages = [18, 19, 20]

for index, name in enumerate(names):
    print(index, name)

print("-----")

for name, age in zip(names, ages):
    print(name, age)