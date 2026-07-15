def process_payment(amount):
    if amount > 0:
        return f"Payment of ₹{amount} Successful"
    else:
        return "Payment Failed"