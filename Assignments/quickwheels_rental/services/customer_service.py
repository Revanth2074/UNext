from data.datastore import DATASTORE
from models.customer import Customer
from typing import List, Optional

def _generate_customer_id() -> str:
    """Helper to generate the next CUxx ID based on existing keys."""
    max_num = 0
    for key in DATASTORE["customers"].keys():
        if key.startswith("CU") and key[2:].isdigit():
            num = int(key[2:])
            if num > max_num:
                max_num = num
    return f"CU{max_num + 1:02d}"

def add_customer(name: str, age: int, phone: str, license_no: str, wallet: float) -> Customer:
    """Adds a new customer to the datastore."""
    cust_id = _generate_customer_id()
    customer = Customer(cust_id, name, age, phone, license_no, wallet)
    DATASTORE["customers"][cust_id] = customer
    return customer

def get_customer(cust_id: str) -> Optional[Customer]:
    """Retrieves a customer by ID."""
    return DATASTORE["customers"].get(cust_id)

def list_customers() -> List[Customer]:
    """Lists all customers in the system."""
    return list(DATASTORE["customers"].values())

def update_phone(cust_id: str, new_phone: str) -> bool:
    """Updates the phone number of a customer."""
    customer = get_customer(cust_id)
    if customer:
        customer.phone = new_phone
        return True
    return False

def delete_customer(cust_id: str) -> bool:
    """Deletes a customer from the datastore."""
    if cust_id in DATASTORE["customers"]:
        del DATASTORE["customers"][cust_id]
        return True
    return False
