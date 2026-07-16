from models.medicine import Medicine
from services.medicine_service import MedicineService


service = MedicineService()

medicine = Medicine(
    101,
    "Paracetamol",
    "Tablet",
    100,
    5
)

service.add_medicine(medicine)

assert service.get_medicine(101).name == "Paracetamol"

service.update_stock(101, 200)

assert service.get_medicine(101).quantity == 200

service.update_price(101, 10)

assert service.get_medicine(101).price == 10

service.delete_medicine(101)

assert service.get_medicine(101) is None

print("Medicine Test Passed")