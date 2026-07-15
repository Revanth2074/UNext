def save_order(cart):

    with open(
        "data/order_history.txt",
        "a"
    ) as file:

        file.write(
            "Order: "
            + ", ".join(cart.view_cart())
            + "\n"
        )


def read_orders():

    try:

        with open(
            "data/order_history.txt",
            "r"
        ) as file:

            return file.read()


    except FileNotFoundError:

        return "No order history found."