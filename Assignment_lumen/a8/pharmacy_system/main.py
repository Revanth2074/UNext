from models.customer import Customer
from models.medicine import Medicine
from models.sale import Sale

from services.pharmacy_system import PharmacySystem


pharmacy = PharmacySystem()

# Add Customer
customer = Customer(
    1,
    "Tony Stark",
    25,
    "Vitamin Tablets"
)

pharmacy.customer_service.add_customer(customer)

# Add Medicines
medicine1 = Medicine(
    101,
    "Paracetamol",
    "Tablet",
    100,
    5
)

medicine2 = Medicine(
    102,
    "Cough Syrup",
    "Syrup",
    50,
    80
)

pharmacy.medicine_service.add_medicine(medicine1)
pharmacy.medicine_service.add_medicine(medicine2)

# Create Sale
sale = Sale(
    1001,
    customer,
    medicine1,
    10,
    "16-07-2026"
)

pharmacy.sale_service.create_sale(sale)

print("\nCustomers")
for customer in pharmacy.customer_service.list_customers():
    print(customer)

print("\nMedicines")
for medicine in pharmacy.medicine_service.list_medicines():
    print(medicine)

print("\nSales")
for sale in pharmacy.sale_service.list_sales():
    print(sale)