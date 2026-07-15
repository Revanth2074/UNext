# id, name, age

class Person:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    def display_info(self):
        print(f"ID: {self.id}, Name: {self.name}, Age: {self.age}")