from services.customer_service import CustomerService
from services.medicine_service import MedicineService
from services.sale_service import SaleService


class PharmacySystem:

    def __init__(self):
        self.customer_service = CustomerService()
        self.medicine_service = MedicineService()
        self.sale_service = SaleService()