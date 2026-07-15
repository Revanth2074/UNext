from banking import accounts

def deposit(name, amount):
    balance = accounts.get_balance(name)
    accounts.update_balance(name, balance + amount)

def withdraw(name, amount):
    balance = accounts.get_balance(name)
    if balance >= amount:
        accounts.update_balance(name, balance - amount)
    else:
        print("Insufficient Balance")

def transfer(sender, receiver, amount):
    if accounts.get_balance(sender) >= amount:
        withdraw(sender, amount)
        deposit(receiver, amount)
    else:
        print("Transfer Failed")