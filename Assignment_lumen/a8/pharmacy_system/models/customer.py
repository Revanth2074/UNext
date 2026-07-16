from models.person import Person


class Customer(Person):

    def __init__(self, customer_id, name, age, prescription):
        super().__init__(customer_id, name, age)
        self.prescription = prescription

    def __str__(self):
        return f"{super().__str__()}, Prescription:{self.prescription}"