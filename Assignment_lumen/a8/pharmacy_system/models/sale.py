class Sale:

    def __init__(self, sale_id, customer, medicine, quantity, date):
        self.id = sale_id
        self.customer = customer
        self.medicine = medicine
        self.quantity = quantity
        self.date = date
        self.total_amount = quantity * medicine.price

    def __str__(self):
        return (
            f"Sale ID:{self.id}\n"
            f"Customer:{self.customer.name}\n"
            f"Medicine:{self.medicine.name}\n"
            f"Quantity:{self.quantity}\n"
            f"Date:{self.date}\n"
            f"Total:{self.total_amount}"
        )