class Person:
    """
    Base class representing a person in the system.
    Handles general attributes for all individuals.
    """
    def __init__(self, person_id: str, name: str, age: int, phone: str):
        self.person_id = person_id
        self.name = name
        self.age = age
        self.phone = phone
