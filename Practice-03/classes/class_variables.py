class Student:
    school = "KBTU"

    def __init__(self, name):
        self.name = name


student1 = Student("Bekzat")
student2 = Student("Sanzhar")

print(student1.school)
print(student2.school)
