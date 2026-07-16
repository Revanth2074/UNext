from models.customer import Customer
from models.medicine import Medicine
from models.sale import Sale

from services.customer_service import CustomerService
from services.medicine_service import MedicineService
from services.sale_service import SaleService


cs = CustomerService()
ms = MedicineService()
ss = SaleService()

customer = Customer(
    1,
    "Tony",
    24,
    "Prescription"
)

medicine = Medicine(
    101,
    "Paracetamol",
    "Tablet",
    100,
    5
)

cs.add_customer(customer)
ms.add_medicine(medicine)

sale = Sale(
    1001,
    customer,
    medicine,
    10,
    "16-07-2026"
)

ss.create_sale(sale)

assert medicine.quantity == 90

assert ss.get_sale(1001).total_amount == 50

print("Sale Test Passed")