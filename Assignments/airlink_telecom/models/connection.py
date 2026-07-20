from models.subscriber import Subscriber
from models.plan import Plan

class Connection:
    """
    Represents a plan connection subscription for a subscriber.
    Uses class-level counter for connection IDs, implements a destructor
    to print archive logs and supports dynamic attributes.
    """
    auto_id_counter = 9001

    def __init__(self, subscriber: Subscriber, plan: Plan, months: int, amount_paid: float, status: str = "ACTIVE"):
        self.connection_id = Connection.auto_id_counter
        Connection.auto_id_counter += 1
        
        self.subscriber = subscriber
        self.plan = plan
        self.months = int(months)
        self.amount_paid = float(amount_paid)
        self.status = status

    def __str__(self) -> str:
        note_str = f" | Note: {getattr(self, 'port_out_note', '')}" if hasattr(self, 'port_out_note') else ""
        return (
            f"--- Receipt for Connection #{self.connection_id} ---\n"
            f"Subscriber: {self.subscriber.name} ({self.subscriber.person_id})\n"
            f"Mobile No : {self.subscriber.mobile_no}\n"
            f"Plan      : {self.plan.plan_id} - {self.plan.name}\n"
            f"Duration  : {self.months} month(s)\n"
            f"Paid      : ₹{self.amount_paid:.2f}\n"
            f"Status    : {self.status}{note_str}\n"
            f"----------------------------------"
        )

    def __del__(self):
        note = getattr(self, "port_out_note", None)
        if note:
            print(f"[ARCHIVE] Connection #{self.connection_id} closed - {note}")
        else:
            print(f"[ARCHIVE] Connection #{self.connection_id} closed")
