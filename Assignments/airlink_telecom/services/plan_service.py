from data.datastore import DATASTORE
from models.plan import Plan, Prepaid, Postpaid, DataPack
from typing import List, Optional

def add_plan(plan_type: str, name: str, data_per_day: float, monthly_price: float) -> Plan:
    """
    Creates and stores a new Plan subclass instance in the datastore.
    Recognized plan types: 'prepaid', 'postpaid', 'datapack' (case-insensitive).
    """
    pt_lower = plan_type.strip().lower()
    if pt_lower == "prepaid":
        plan = Prepaid(name, data_per_day, monthly_price)
    elif pt_lower == "postpaid":
        plan = Postpaid(name, data_per_day, monthly_price)
    elif pt_lower == "datapack":
        plan = DataPack(name, data_per_day, monthly_price)
    else:
        raise ValueError(f"Unknown plan type: {plan_type}. Must be Prepaid, Postpaid, or DataPack.")

    DATASTORE["plans"][plan.plan_id] = plan
    return plan

def get_plan(plan_id: str) -> Optional[Plan]:
    """Retrieves a plan by ID."""
    return DATASTORE["plans"].get(plan_id)

def list_plans() -> List[Plan]:
    """Lists all plans in the system."""
    return list(DATASTORE["plans"].values())

def delete_plan(plan_id: str) -> bool:
    """Deletes a plan from the datastore."""
    if plan_id in DATASTORE["plans"]:
        del DATASTORE["plans"][plan_id]
        return True
    return False

def apply_festival_offer(plan_id: str, pct: float) -> bool:
    """
    Applies a percentage discount to the specified plan using setattr.
    Returns True if successful, False if the plan was not found.
    """
    plan = get_plan(plan_id)
    if plan:
        if pct < 0 or pct > 100:
            raise ValueError("Festival offer percentage must be between 0 and 100.")
        setattr(plan, "festival_offer", float(pct))
        return True
    return False
