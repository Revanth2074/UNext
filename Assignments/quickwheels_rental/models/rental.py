from models.customer import Customer
from models.vehicle import Vehicle

class Rental:
    """
    Represents a vehicle rental transaction.
    Uses class-level counter starting from 5001.
    Implements a destructor that prints archive logs.
    """
    auto_id_counter = 5001

    def __init__(self, customer: Customer, vehicle: Vehicle, planned_days: int, amount_paid: float, deposit: float, status: str = "ACTIVE"):
        self.rental_id = Rental.auto_id_counter
        Rental.auto_id_counter += 1

        self.customer = customer
        self.vehicle = vehicle
        self.planned_days = int(planned_days)
        self.amount_paid = float(amount_paid)
        self.deposit = float(deposit)
        self.status = status

    def __str__(self) -> str:
        note_str = f" | Damage: {getattr(self, 'damage_note', '')}" if hasattr(self, 'damage_note') else ""
        return (
            f"--- Invoice for Rental #{self.rental_id} ---\n"
            f"Customer  : {self.customer.name} ({self.customer.person_id})\n"
            f"Vehicle   : {self.vehicle.vehicle_id} - {self.vehicle.name}\n"
            f"Duration  : {self.planned_days} day(s)\n"
            f"Paid Cost : ₹{self.amount_paid:.2f}\n"
            f"Deposit   : ₹{self.deposit:.2f}\n"
            f"Status    : {self.status}{note_str}\n"
            f"----------------------------------"
        )

    def __del__(self):
        note = getattr(self, "damage_note", None)
        if note:
            print(f"[ARCHIVE] Rental #{self.rental_id} closed - {note}")
        else:
            print(f"[ARCHIVE] Rental #{self.rental_id} closed")
