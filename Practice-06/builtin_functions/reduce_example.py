from functools import reduce

numbers = [1, 2, 3, 4, 5]

total = reduce(lambda x, y: x + y, numbers)

product = reduce(lambda x, y: x * y, numbers)

print("Numbers:", numbers)
print("Sum:", total)
print("Product:", product)