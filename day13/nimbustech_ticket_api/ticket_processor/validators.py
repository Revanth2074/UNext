"""Validators for ticket fields and raw CSV rows."""

from datetime import datetime
from typing import Tuple, Dict, Any
from ticket_processor.config import PRIORITY_MAP, DATE_FORMAT


def validate_row(row: Dict[str, str]) -> Tuple[bool, str | None]:
    """Validates a single CSV row containing ticket information.

    A row is valid if:
    - ticket_id is present
    - customer_name is present
    - sla_hours is a positive number (> 0)
    - created_at is parseable as a date
    - priority_raw is one of: low, medium, high, critical

    Args:
        row (dict): A dictionary representing the CSV row.

    Returns:
        tuple: (is_valid: bool, error_reason: str or None)
    """
    # 1. Validate ticket_id
    ticket_id = row.get("ticket_id")
    if not ticket_id or not ticket_id.strip():
        return False, "missing ticket_id"

    # 2. Validate customer_name
    customer_name = row.get("customer_name")
    if not customer_name or not customer_name.strip():
        return False, "missing customer_name"

    # 3. Validate priority_raw
    priority_raw = row.get("priority_raw")
    if not priority_raw:
        return False, "missing priority_raw"
    
    priority_clean = priority_raw.strip().lower()
    if priority_clean not in PRIORITY_MAP:
        return False, f"invalid priority_raw: '{priority_raw}'"

    # 4. Validate created_at
    created_at_str = row.get("created_at")
    if not created_at_str or not created_at_str.strip():
        return False, "missing created_at"

    try:
        datetime.strptime(created_at_str.strip(), DATE_FORMAT)
    except ValueError:
        return False, f"invalid created_at date format: '{created_at_str}'"

    # 5. Validate sla_hours
    sla_hours_str = row.get("sla_hours")
    if not sla_hours_str or not sla_hours_str.strip():
        return False, "missing sla_hours"

    try:
        sla_hours = float(sla_hours_str.strip())
        if sla_hours <= 0:
            return False, f"sla_hours must be a positive number: {sla_hours_str}"
    except ValueError:
        return False, f"sla_hours is not a valid number: '{sla_hours_str}'"

    # 6. Validate status (optional: make sure it is not empty)
    status = row.get("status")
    if not status or not status.strip():
        return False, "missing status"

    return True, None
