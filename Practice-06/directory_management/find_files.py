import os

path = "."

for file in os.listdir(path):
    if file.endswith(".py") and os.path.isfile(os.path.join(path, file)):
        print(file)