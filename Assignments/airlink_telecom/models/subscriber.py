from models.person import Person

class Subscriber(Person):
    """
    Subscriber class inheriting from Person.
    Implements mobile subscription data and balance encapsulation.
    """
    def __init__(self, person_id: str, name: str, age: int, phone: str, mobile_no: str, id_proof: str, balance: float):
        super().__init__(person_id, name, age, phone)
        self.mobile_no = mobile_no
        self.id_proof = id_proof
        self.__balance = float(balance)

    @property
    def balance(self) -> float:
        """Read-only property for subscriber's balance."""
        return self.__balance

    def recharge(self, amount: float) -> None:
        """Increase the subscriber's balance."""
        if amount > 0:
            self.__balance += amount

    def deduct(self, amount: float) -> bool:
        """
        Deduct the specified amount from the balance if funds are sufficient.
        Returns True if successful, False otherwise (leaving balance unchanged).
        """
        if amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
