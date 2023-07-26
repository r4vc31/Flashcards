class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f'Hello, I am {self.name}!'

data = input()
person_1 = Person(data)
print(person_1.greet())
