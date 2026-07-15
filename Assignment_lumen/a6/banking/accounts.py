accounts = {}

def create_account(name, balance=0):
    accounts[name] = balance

def get_balance(name):
    return accounts.get(name, 0)

def update_balance(name, balance):
    accounts[name] = balance