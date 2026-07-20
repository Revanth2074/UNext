from models.subscriber import Subscriber
from data.datastore import DATASTORE

def is_eligible(subscriber: Subscriber) -> bool:
    """
    Validates subscriber eligibility.
    Subscriber must be at least 18 years old and have a valid ID proof (not 'none', '(none)', or empty).
    """
    if subscriber.age < 18:
        return False
    if not subscriber.id_proof:
        return False
    # Check for placeholder strings like 'none' or '(none)'
    id_clean = subscriber.id_proof.strip().lower()
    if id_clean in ("none", "(none)", ""):
        return False
    return True

def has_active_connection(sub_id: str) -> bool:
    """
    Checks if a subscriber already has an active connection in the datastore.
    One-active-connection rule: a subscriber can only have one active connection.
    """
    for conn in DATASTORE["connections"].values():
        if conn.subscriber.person_id == sub_id and conn.status == "ACTIVE":
            return True
    return False

def positive_int(value) -> bool:
    """
    Checks if the value is or represents a positive integer greater than 0.
    """
    try:
        val = int(value)
        return val > 0
    except (ValueError, TypeError):
        return False
