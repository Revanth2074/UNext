from data.datastore import DATASTORE
from models.subscriber import Subscriber
from typing import List, Optional

def _generate_subscriber_id() -> str:
    """Helper to generate the next SUBxx ID based on existing keys."""
    max_num = 0
    for key in DATASTORE["subscribers"].keys():
        if key.startswith("SUB") and key[3:].isdigit():
            num = int(key[3:])
            if num > max_num:
                max_num = num
    return f"SUB{max_num + 1:02d}"

def add_subscriber(name: str, age: int, phone: str, mobile_no: str, id_proof: str, balance: float) -> Subscriber:
    """Adds a new subscriber to the datastore."""
    sub_id = _generate_subscriber_id()
    subscriber = Subscriber(sub_id, name, age, phone, mobile_no, id_proof, balance)
    DATASTORE["subscribers"][sub_id] = subscriber
    return subscriber

def get_subscriber(sub_id: str) -> Optional[Subscriber]:
    """Retrieves a subscriber by ID."""
    return DATASTORE["subscribers"].get(sub_id)

def list_subscribers() -> List[Subscriber]:
    """Lists all subscribers in the system."""
    return list(DATASTORE["subscribers"].values())

def update_phone(sub_id: str, new_phone: str) -> bool:
    """Updates the phone number of a subscriber."""
    subscriber = get_subscriber(sub_id)
    if subscriber:
        subscriber.phone = new_phone
        return True
    return False

def delete_subscriber(sub_id: str) -> bool:
    """Deletes a subscriber from the datastore."""
    if sub_id in DATASTORE["subscribers"]:
        del DATASTORE["subscribers"][sub_id]
        return True
    return False
