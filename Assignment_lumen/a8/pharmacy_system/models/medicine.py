class Medicine:

    def __init__(self, medicine_id, name, med_type, quantity, price):
        self.id = medicine_id
        self.name = name
        self.type = med_type
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return (
            f"ID:{self.id}, "
            f"Name:{self.name}, "
            f"Type:{self.type}, "
            f"Stock:{self.quantity}, "
            f"Price:{self.price}"
        )