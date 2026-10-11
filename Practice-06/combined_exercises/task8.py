import os

path = "destination.txt"

if os.path.isfile(path):
    if os.access(path, os.W_OK):
        try:
            os.remove(path)
            print("File deleted successfully!")
        except OSError as error:
            print("Cannot delete file:", error)
    else:
        print("No write permission!")
else:
    print("File does not exist!")