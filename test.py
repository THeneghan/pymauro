#Test ground

class Student:
    wey=9
    def __init__(self,name,age=None):
        self.name=name
        self.age=age


val = Student("TOm",77)
print(val.age)
val2=Student("james")
print(val2.age)


import testconnection
print(testconnection.__doc__)

