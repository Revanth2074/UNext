from ecommerce import cart, payment

cart.add_item("Laptop", 50000)
cart.add_item("Mouse", 800)

print("Cart:", cart.view_cart())

total = cart.calculate_total()
print("Total =", total)

print(payment.process_payment(total))