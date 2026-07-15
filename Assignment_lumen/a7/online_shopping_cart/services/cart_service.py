from exceptions.cart_exceptions import (
    OutOfStockError,
    EmptyCartError
)


class CartService:


    # Add product into cart
    def add_to_cart(self, user, product, quantity):

        if product.quantity < quantity:

            raise OutOfStockError(
                "Error: Product is out of stock."
            )


        product.reduce_stock(quantity)


        user.cart.add_product(
            product,
            quantity
        )


        print(
            "Product added to cart successfully."
        )



    # Remove product from cart
    def remove_from_cart(self, user, product_name):

        result = user.cart.remove_product(
            product_name
        )


        if result:

            print(
                "Product removed from cart."
            )

        else:

            print(
                "Product not found in cart."
            )



    # View cart
    def display_cart(self, user):

        cart = user.cart.view_cart()


        if len(cart) == 0:

            print(
                "Cart is empty."
            )

            return


        print("\nShopping Cart")

        for item in cart:

            print(item)


        print(
            "Total Amount: ₹",
            user.cart.calculate_total()
        )



    # Checkout
    def checkout(self, user):

        if len(user.cart.items) == 0:

            raise EmptyCartError(
                "Error: Cart is empty."
            )


        total = user.checkout()


        print(
            f"Order placed successfully."
        )

        print(
            f"Total Paid: ₹{total}"
        )


        user.cart.clear_cart()