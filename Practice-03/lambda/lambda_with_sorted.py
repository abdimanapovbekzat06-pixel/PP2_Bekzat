students = [
    ("Alice", 85),
    ("Bob", 70),
    ("Charlie", 95)
]

result = sorted(students, key=lambda x: x[1])

print(*result)
