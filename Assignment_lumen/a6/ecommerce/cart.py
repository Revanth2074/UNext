cart_items = []

def add_item(item, price):
    cart_items.append((item, price))

def remove_item(item):
    global cart_items
    cart_items = [i for i in cart_items if i[0] != item]

def calculate_total():
    return sum(price for item, price in cart_items)

def view_cart():
    return cart_items