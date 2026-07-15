import unittest

from models.product import Product
from models.user import User
from models.premium_user import PremiumUser

from services.cart_service import CartService

from exceptions.cart_exceptions import (
    OutOfStockError,
    EmptyCartError
)


class TestShoppingCart(unittest.TestCase):


    def setUp(self):

        self.cart_service = CartService()

        self.product = Product(
            "Laptop",
            50000,
            5
        )

        self.mouse = Product(
            "Mouse",
            1000,
            2
        )

        self.user = User(
            "Alice"
        )


    # Test adding product to cart
    def test_add_product(self):

        self.cart_service.add_to_cart(
            self.user,
            self.product,
            1
        )

        self.assertEqual(
            len(self.user.cart.items),
            1
        )


    # Test total calculation
    def test_cart_total(self):

        self.cart_service.add_to_cart(
            self.user,
            self.product,
            2
        )

        total = self.user.cart.calculate_total()

        self.assertEqual(
            total,
            100000
        )


    # Test removing product
    def test_remove_product(self):

        self.cart_service.add_to_cart(
            self.user,
            self.product,
            1
        )


        self.cart_service.remove_from_cart(
            self.user,
            "Laptop"
        )


        self.assertEqual(
            len(self.user.cart.items),
            0
        )


    # Test out of stock
    def test_out_of_stock(self):

        with self.assertRaises(
            OutOfStockError
        ):

            self.cart_service.add_to_cart(
                self.user,
                self.product,
                10
            )


    # Test empty checkout
    def test_empty_cart_checkout(self):

        with self.assertRaises(
            EmptyCartError
        ):

            self.cart_service.checkout(
                self.user
            )


    # Test premium user discount
    def test_premium_user(self):

        premium = PremiumUser(
            "Bob",
            10
        )


        premium.cart.add_product(
            self.product,
            1
        )


        amount = premium.checkout()


        self.assertEqual(
            amount,
            45000
        )



if __name__ == "__main__":

    unittest.main()