from models.user import User


class PremiumUser(User):

    def __init__(self, name, discount=10):
        super().__init__(name)
        self.discount = discount


    def checkout(self):

        total = self.cart.calculate_total()

        discount_amount = (
            total * self.discount / 100
        )

        return total - discount_amount