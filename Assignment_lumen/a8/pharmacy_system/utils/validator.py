def stock_available(medicine, quantity):
    return medicine.quantity >= quantity


def valid_age(age):
    return age > 0