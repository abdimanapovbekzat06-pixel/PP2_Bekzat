import os

if os.path.exists("copy.txt"):
    os.remove("copy.txt")
    print("File deleted successfully!")
else:
    print("File does not exist!")