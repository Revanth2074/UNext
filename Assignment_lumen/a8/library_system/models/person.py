class Person:
    def __init__(self, member_id, name, age):
        self.id = member_id
        self.name = name
        self.age = age

    def __str__(self):
        return f"ID:{self.id}, Name:{self.name}, Age:{self.age}"