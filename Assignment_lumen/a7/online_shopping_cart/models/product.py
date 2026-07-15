class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def reduce_stock(self, amount):
        self.quantity -= amount

    def increase_stock(self, amount):
        self.quantity += amount

    def get_details(self):
        return {
            "Name": self.name,
            "Price": self.price,
            "Available Quantity": self.quantity
        }

    def __str__(self):
        return f"{self.name} - ₹{self.price}"