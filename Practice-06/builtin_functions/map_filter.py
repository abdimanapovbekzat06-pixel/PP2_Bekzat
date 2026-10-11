numbers = [1, 2, 3, 4, 5, 6]

squared = list(map(lambda x: x * x, numbers))

even = list(filter(lambda x: x % 2 == 0, numbers))

print("Original:", numbers)
print("Squared:", squared)
print("Even numbers:", even)