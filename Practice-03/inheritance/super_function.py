class Animal:
    def speak(self):
        print("Animal makes a sound")


class Dog(Animal):
    def speak(self):
        super().speak()
        print("Dog says Woof!")


dog = Dog()
dog.speak()
