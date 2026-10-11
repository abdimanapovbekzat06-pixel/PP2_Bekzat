import os

path = "task1.py"

if os.path.exists(path):
    print("Path exists")
    print("Filename:", os.path.basename(path))
    print("Directory:", os.path.dirname(os.path.abspath(path)))
else:
    print("Path does not exist")