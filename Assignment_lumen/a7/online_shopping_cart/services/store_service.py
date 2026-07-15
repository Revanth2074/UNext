from exceptions.cart_exceptions import ProductNotFoundError


class StoreService:

    def __init__(self):
        self.products = []


    # Add product to store
    def add_product(self, product):

        self.products.append(product)

        print(
            f"{product.name} added to store."
        )


    # Display available products
    def view_products(self):

        print("\nAvailable Products")

        for product in self.products:

            print(
                f"Name: {product.name}"
            )

            print(
                f"Price: ₹{product.price}"
            )

            print(
                f"Stock: {product.quantity}"
            )

            print("-------------------")


    # Search product
    def find_product(self, name):

        for product in self.products:

            if product.name.lower() == name.lower():

                return product


        raise ProductNotFoundError(
            "Error: Product not found."
        )


    # Update inventory
    def update_stock(self, name, quantity):

        product = self.find_product(name)

        product.quantity += quantity