with open("sample.txt", "w") as file:
    file.write("Hello World\n")
    file.write("I am learning Python\n")
    file.write("This is Practice 6\n")

with open("sample.txt", "r") as file:
    lines = file.readlines()

print("Number of lines:", len(lines))