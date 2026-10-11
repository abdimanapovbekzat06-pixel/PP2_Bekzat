import os

os.makedirs("letters", exist_ok=True)

for i in range(65, 91):
    letter = chr(i)

    with open(f"letters/{letter}.txt", "w") as file:
        file.write(f"This is file {letter}.txt")

print("26 files created successfully!")