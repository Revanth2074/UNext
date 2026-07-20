from data.datastore import DATASTORE
import services.subscriber_service as sub_service
import services.plan_service as plan_service
import services.connection_service as conn_service
import data.seed_data as seed
from models.subscriber import Subscriber
from models.plan import Plan
from models.connection import Connection
from typing import List, Optional

class TelecomSystem:
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

    # Subscriber methods
    def register_subscriber(self, name: str, age: int, phone: str, mobile_no: str, id_proof: str, balance: float) -> Subscriber:
        return sub_service.add_subscriber(name, age, phone, mobile_no, id_proof, balance)

    def get_subscriber(self, sub_id: str) -> Optional[Subscriber]:
        return sub_service.get_subscriber(sub_id)

    def list_subscribers(self) -> List[Subscriber]:
        return sub_service.list_subscribers()

    def update_subscriber_phone(self, sub_id: str, new_phone: str) -> bool:
        return sub_service.update_phone(sub_id, new_phone)

    def delete_subscriber(self, sub_id: str) -> bool:
        return sub_service.delete_subscriber(sub_id)

    # Plan methods
    def add_plan(self, plan_type: str, name: str, data_per_day: float, monthly_price: float) -> Plan:
        return plan_service.add_plan(plan_type, name, data_per_day, monthly_price)

    def get_plan(self, plan_id: str) -> Optional[Plan]:
        return plan_service.get_plan(plan_id)

    def list_plans(self) -> List[Plan]:
        return plan_service.list_plans()

    def delete_plan(self, plan_id: str) -> bool:
        return plan_service.delete_plan(plan_id)

    def apply_festival_offer(self, plan_id: str, pct: float) -> bool:
        return plan_service.apply_festival_offer(plan_id, pct)

    # Connection methods
    def activate_connection(self, sub_id: str, plan_id: str, months: int) -> Connection:
        return conn_service.activate(sub_id, plan_id, months)

    def deactivate_connection(self, conn_id: int, used_months: int, port_out: bool = False) -> float:
        return conn_service.deactivate(conn_id, used_months, port_out)

    def get_connection(self, conn_id: int) -> Optional[Connection]:
        return conn_service.get_connection(conn_id)

    def list_connections(self) -> List[Connection]:
        return conn_service.list_connections()

    def delete_connection(self, conn_id: int) -> bool:
        return conn_service.delete_connection(conn_id)

    def exit_system(self) -> None:
        """
        Clears connections in the datastore, releasing their references
        so that connection object destructors (__del__) are triggered.
        """
        DATASTORE["connections"].clear()
