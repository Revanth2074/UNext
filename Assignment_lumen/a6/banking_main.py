from banking import accounts, transactions

accounts.create_account("Asha", 5000)
accounts.create_account("Bala", 3000)

transactions.deposit("Asha", 1000)
transactions.withdraw("Bala", 500)
transactions.transfer("Asha", "Bala", 2000)

print("Asha Balance =", accounts.get_balance("Asha"))
print("Bala Balance =", accounts.get_balance("Bala"))