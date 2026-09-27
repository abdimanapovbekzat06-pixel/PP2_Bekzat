def numbers():
    for i in range(1, 6):
        yield i

for x in numbers():
    print(x)