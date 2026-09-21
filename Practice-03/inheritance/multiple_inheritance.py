class Father:
    def work(self):
        print("Father is working")


class Mother:
    def cook(self):
        print("Mother is cooking")


class Child(Father, Mother):
    pass


child = Child()

child.work()
child.cook()
