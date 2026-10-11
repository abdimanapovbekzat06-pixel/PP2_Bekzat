with open("source.txt", "w") as file:
    file.write("Hello Python!\n")
    file.write("This is Practice 6.")

with open("source.txt", "r") as file:
    content = file.read()

with open("destination.txt", "w") as file:
    file.write(content)

print("File contents copied successfully!")