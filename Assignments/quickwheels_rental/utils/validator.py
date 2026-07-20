from models.customer import Customer
from models.vehicle import Vehicle

def is_eligible(customer: Customer) -> bool:
    """
    Validates customer eligibility.
    Customer must be at least 18 years old and have a valid license (not 'none', '(none)', or empty).
    """
    if customer.age < 18:
        return False
    if not customer.license_no:
        return False
    license_clean = customer.license_no.strip().lower()
    if license_clean in ("none", "(none)", ""):
        return False
    return True

def is_available(vehicle: Vehicle) -> bool:
    """
    Checks if a vehicle is available for rent.
    """
    return bool(vehicle.available)

def positive_int(value) -> bool:
    """
    Checks if the value is or represents a positive integer greater than 0.
    """
    try:
        val = int(value)
        return val > 0
    except (ValueError, TypeError):
        return False
