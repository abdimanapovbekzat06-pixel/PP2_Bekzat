import os

path = "."

items = os.listdir(path)

print("Directories:")
for item in items:
    if os.path.isdir(os.path.join(path, item)):
        print(item)

print("Files:")
for item in items:
    if os.path.isfile(os.path.join(path, item)):
        print(item)

print("All:")
for item in items:
    print(item)