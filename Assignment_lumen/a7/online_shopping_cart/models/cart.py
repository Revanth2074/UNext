class Cart:

    def __init__(self):
        self.items = []


    def add_product(self, product, quantity):

        self.items.append({
            "product": product,
            "quantity": quantity
        })


    def remove_product(self, product_name):

        for item in self.items:

            if item["product"].name == product_name:
                self.items.remove(item)
                return True

        return False


    def calculate_total(self):

        total = 0

        for item in self.items:

            total += (
                item["product"].price *
                item["quantity"]
            )

        return total


    def view_cart(self):

        cart_details = []

        for item in self.items:

            cart_details.append(
                f"{item['product'].name} x {item['quantity']}"
            )

        return cart_details


    def clear_cart(self):
        self.items.clear()