from data.datastore import DATASTORE
from models.connection import Connection
import services.subscriber_service as subscriber_service
import services.plan_service as plan_service
import utils.validator as validator
from typing import List, Optional

def activate(sub_id: str, plan_id: str, months: int) -> Connection:
    """
    Activates a new connection for a subscriber.
    Validates eligibility, active connections, and debit fees.
    """
    subscriber = subscriber_service.get_subscriber(sub_id)
    if not subscriber:
        raise ValueError(f"Subscriber {sub_id} not found.")

    plan = plan_service.get_plan(plan_id)
    if not plan:
        raise ValueError(f"Plan {plan_id} not found.")

    if not validator.is_eligible(subscriber):
        raise ValueError(f"Subscriber {sub_id} is ineligible (must be age 18+ and have ID proof).")

    if validator.has_active_connection(sub_id):
        raise ValueError(f"Subscriber {sub_id} already has an active connection.")

    if not validator.positive_int(months):
        raise ValueError("Duration in months must be a positive integer.")

    months = int(months)
    # Calculate costs
    cost = plan.bill(months) + plan.activation_fee

    # Charge subscriber
    if not subscriber.deduct(cost):
        raise ValueError(
            f"Insufficient balance. Cost is ₹{cost:.2f} (bill: ₹{plan.bill(months):.2f} + activation fee: ₹{plan.activation_fee:.2f}), "
            f"but current balance is ₹{subscriber.balance:.2f}."
        )

    # Create connection
    connection = Connection(subscriber, plan, months, cost, status="ACTIVE")
    DATASTORE["connections"][connection.connection_id] = connection
    return connection

def deactivate(conn_id: int, used_months: int, port_out: bool = False) -> float:
    """
    Deactivates an active connection and processes refund.
    Refund = max(0, (months - used_months) * price * 0.5 - 150 if port_out).
    Credits refund to subscriber balance.
    """
    conn_key = int(conn_id)
    connection = DATASTORE["connections"].get(conn_key)
    if not connection:
        raise ValueError(f"Connection #{conn_id} not found.")

    if connection.status == "DEACTIVATED":
        raise ValueError(f"Connection #{conn_id} is already deactivated.")

    used_months = int(used_months)
    if used_months < 0 or used_months > connection.months:
        raise ValueError(f"Used months must be between 0 and {connection.months}.")

    price = connection.plan.monthly_price
    months = connection.months
    
    # Calculate refund
    base_refund = (months - used_months) * price * 0.5
    if port_out:
        refund = max(0.0, base_refund - 150.0)
    else:
        refund = max(0.0, base_refund)

    # Recharge subscriber
    connection.subscriber.recharge(refund)
    connection.status = "DEACTIVATED"

    # Attach optional port out note via setattr
    if port_out:
        setattr(connection, "port_out_note", "Porting out")

    return refund

def get_connection(conn_id: int) -> Optional[Connection]:
    """Retrieves a connection by ID."""
    return DATASTORE["connections"].get(int(conn_id))

def list_connections() -> List[Connection]:
    """Lists all connections in the system."""
    return list(DATASTORE["connections"].values())

def delete_connection(conn_id: int) -> bool:
    """Deletes a connection from the datastore."""
    conn_key = int(conn_id)
    if conn_key in DATASTORE["connections"]:
        del DATASTORE["connections"][conn_key]
        return True
    return False
