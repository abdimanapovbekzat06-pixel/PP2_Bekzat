with open("sample.txt", "a") as file:
    file.write("\nPython is easy!")
    file.write("\nI am learning file handling")

with open("sample.txt", "r") as file:
    print(file.read())