from data.datastore import DATASTORE
import services.customer_service as cust_service
import services.vehicle_service as veh_service
import services.rental_service as rent_service
import data.seed_data as seed
from models.customer import Customer
from models.vehicle import Vehicle
from models.rental import Rental
from typing import List, Optional

class RentalSystem:
    """
    Orchestrator class following the 'real-project layering' design.
    The menu interface talks only to this class.
    """
    def __init__(self, load_seed: bool = True):
        if load_seed:
            self.seed_system()

    def seed_system(self) -> None:
        """Loads default seed data into the system."""
        seed.seed_data()

    # Customer methods
    def register_customer(self, name: str, age: int, phone: str, license_no: str, wallet: float) -> Customer:
        return cust_service.add_customer(name, age, phone, license_no, wallet)

    def get_customer(self, cust_id: str) -> Optional[Customer]:
        return cust_service.get_customer(cust_id)

    def list_customers(self) -> List[Customer]:
        return cust_service.list_customers()

    def update_customer_phone(self, cust_id: str, new_phone: str) -> bool:
        return cust_service.update_phone(cust_id, new_phone)

    def delete_customer(self, cust_id: str) -> bool:
        return cust_service.delete_customer(cust_id)

    # Vehicle methods
    def add_vehicle(self, vehicle_type: str, name: str, daily_rate: float) -> Vehicle:
        return veh_service.add_vehicle(vehicle_type, name, daily_rate)

    def get_vehicle(self, vehicle_id: str) -> Optional[Vehicle]:
        return veh_service.get_vehicle(vehicle_id)

    def list_vehicles(self) -> List[Vehicle]:
        return veh_service.list_vehicles()

    def delete_vehicle(self, vehicle_id: str) -> bool:
        return veh_service.delete_vehicle(vehicle_id)

    def apply_festival_offer(self, vehicle_id: str, pct: float) -> bool:
        return veh_service.apply_festival_offer(vehicle_id, pct)

    # Rental methods
    def rent_vehicle(self, cust_id: str, veh_id: str, days: int) -> Rental:
        return rent_service.rent(cust_id, veh_id, days)

    def return_vehicle(self, rental_id: int, actual_days: int, damage_note: Optional[str] = None) -> float:
        return rent_service.return_vehicle(rental_id, actual_days, damage_note)

    def get_rental(self, rental_id: int) -> Optional[Rental]:
        return rent_service.get_rental(rental_id)

    def list_rentals(self) -> List[Rental]:
        return rent_service.list_rentals()

    def delete_rental(self, rental_id: int) -> bool:
        return rent_service.delete_rental(rental_id)

    def exit_system(self) -> None:
        """
        Clears rentals in the datastore, releasing their references
        so that rental object destructors (__del__) are triggered.
        """
        DATASTORE["rentals"].clear()
