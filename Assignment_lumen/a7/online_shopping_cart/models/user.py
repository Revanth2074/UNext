from models.cart import Cart


class User:

    def __init__(self, name):
        self.name = name
        self.cart = Cart()


    def view_cart(self):

        return self.cart.view_cart()


    def checkout(self):

        return self.cart.calculate_total()