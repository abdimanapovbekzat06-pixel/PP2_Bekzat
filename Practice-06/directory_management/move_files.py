import os
import shutil

os.makedirs("folder1", exist_ok=True)
os.makedirs("folder2", exist_ok=True)

with open("folder1/test.txt", "w") as file:
    file.write("Hello Python!")

shutil.copy("folder1/test.txt", "folder2/test.txt")

shutil.move("folder1/test.txt", "folder1/moved.txt")

print("Files copied and moved successfully!")