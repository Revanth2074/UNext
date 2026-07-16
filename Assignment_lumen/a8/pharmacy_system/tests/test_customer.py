from models.customer import Customer
from services.customer_service import CustomerService


service = CustomerService()

customer = Customer(
    1,
    "Tony",
    25,
    "Paracetamol"
)

service.add_customer(customer)

assert service.get_customer(1).name == "Tony"

service.update_prescription(1, "Amoxicillin")

assert service.get_customer(1).prescription == "Amoxicillin"

service.delete_customer(1)

assert service.get_customer(1) is None

print("Customer Test Passed")