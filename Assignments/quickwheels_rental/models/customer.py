from models.person import Person

class Customer(Person):
    """
    Customer class inheriting from Person.
    Implements wallet balance encapsulation and pay/deposit logic.
    """
    def __init__(self, person_id: str, name: str, age: int, phone: str, license_no: str, wallet: float):
        super().__init__(person_id, name, age, phone)
        self.license_no = license_no
        self.__wallet = float(wallet)

    @property
    def balance(self) -> float:
        """Read-only property for customer's wallet balance."""
        return self.__wallet

    def add_money(self, amount: float) -> None:
        """Increase the customer's wallet balance."""
        if amount > 0:
            self.__wallet += amount

    def pay(self, amount: float) -> bool:
        """
        Deduct the specified amount from the wallet if funds are sufficient.
        Returns True if successful, False otherwise.
        """
        if amount <= self.__wallet:
            self.__wallet -= amount
            return True
        return False
