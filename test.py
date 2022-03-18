#Test ground

class Student:
    def __init__(self):
        self._name=None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

Val=Student()
Val.name="Hello"
print(Val.name)
