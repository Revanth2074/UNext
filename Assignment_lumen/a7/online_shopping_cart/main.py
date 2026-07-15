from models.product import Product
from models.user import User
from models.premium_user import PremiumUser

from services.store_service import StoreService
from services.cart_service import CartService

from exceptions.cart_exceptions import (
    OutOfStockError,
    ProductNotFoundError,
    EmptyCartError
)

from utils.file_handler import save_order, read_orders



store = StoreService()

cart_service = CartService()



# Create products

laptop = Product(
    "Laptop",
    60000,
    5
)

mouse = Product(
    "Mouse",
    1000,
    10
)

keyboard = Product(
    "Keyboard",
    2500,
    7
)



store.add_product(laptop)
store.add_product(mouse)
store.add_product(keyboard)



# Create users

user = User("Alice")

premium_user = PremiumUser(
    "Bob"
)



def menu():

    while True:

        print(
            "\n====== Online Shopping Cart System ======"
        )

        print(
            "1. View Products"
        )

        print(
            "2. Add Product to Cart"
        )

        print(
            "3. Remove Product from Cart"
        )

        print(
            "4. View Cart"
        )

        print(
            "5. Checkout"
        )

        print(
            "6. View Order History"
        )

        print(
            "7. Exit"
        )


        choice = input(
            "Enter your choice: "
        )


        try:


            if choice == "1":

                store.view_products()



            elif choice == "2":

                name = input(
                    "Enter product name: "
                )

                quantity = int(
                    input(
                        "Enter quantity: "
                    )
                )


                product = store.find_product(
                    name
                )


                cart_service.add_to_cart(
                    user,
                    product,
                    quantity
                )



            elif choice == "3":

                name = input(
                    "Enter product name to remove: "
                )


                cart_service.remove_from_cart(
                    user,
                    name
                )



            elif choice == "4":

                cart_service.display_cart(
                    user
                )



            elif choice == "5":

                cart_service.checkout(
                    user
                )

                save_order(
                    user.cart
                )



            elif choice == "6":

                print(
                    read_orders()
                )



            elif choice == "7":

                print(
                    "Thank you for shopping!"
                )

                break



            else:

                print(
                    "Invalid choice."
                )



        except OutOfStockError as e:

            print(e)



        except ProductNotFoundError as e:

            print(e)



        except EmptyCartError as e:

            print(e)



        except Exception as e:

            print(
                "Error:",
                e
            )



if __name__ == "__main__":

    menu()