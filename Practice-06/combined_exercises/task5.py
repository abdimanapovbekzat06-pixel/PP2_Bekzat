fruits = ["Apple", "Banana", "Orange", "Mango"]

with open("fruits.txt", "w") as file:
    for fruit in fruits:
        file.write(fruit + "\n")

with open("fruits.txt", "r") as file:
    print(file.read())