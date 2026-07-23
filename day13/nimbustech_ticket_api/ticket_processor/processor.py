"""Core logic for processing tickets CSV and generating report."""

import csv
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
from ticket_processor.config import PRIORITY_MAP, DATE_FORMAT, CLOSED_STATUSES, MAX_INVALID_RATIO
from ticket_processor.models import Ticket
from ticket_processor.validators import validate_row


def process_tickets(
    csv_content_lines: List[str], now: datetime
) -> Tuple[Dict[str, Any], bool]:
    """Processes ticket CSV lines, validates them, detects SLA breaches,

    and builds the summary report.

    Args:
        csv_content_lines (list of str): Raw lines of the CSV file.
        now (datetime): The current datetime acting as "now" for SLA breach checks.

    Returns:
        tuple: (report: dict, is_aborted: bool)
    """
    if not csv_content_lines:
        return {
            "generated_at": now.isoformat(),
            "summary": {
                "total_rows": 0,
                "valid_tickets": 0,
                "invalid_rows": 0,
                "breached_count": 0,
                "by_category": {},
            },
            "tickets": [],
            "invalid_rows": [],
        }, False

    # Read header and data lines using csv reader to handle quotes/commas properly
    reader = csv.reader(csv_content_lines)
    try:
        header = next(reader)
    except StopIteration:
        return {
            "generated_at": now.isoformat(),
            "summary": {
                "total_rows": 0,
                "valid_tickets": 0,
                "invalid_rows": 0,
                "breached_count": 0,
                "by_category": {},
            },
            "tickets": [],
            "invalid_rows": [],
        }, False

    header = [h.strip() for h in header]

    tickets: List[Ticket] = []
    invalid_rows_info: List[Dict[str, str]] = []
    category_counts: Dict[str, int] = {}
    breached_count = 0

    total_rows = 0

    # Process each line
    for idx, row_values in enumerate(reader, start=1):
        total_rows += 1
        # Get raw line corresponding to this row (index idx in csv_content_lines, since index 0 was header)
        # Note: If there are multi-line fields in CSV, indexing might not align perfectly, 
        # but for this script and sample, lines correspond 1:1.
        raw_line = ""
        if idx < len(csv_content_lines):
            raw_line = csv_content_lines[idx].strip("\r\n")

        # Create row dict mapping headers to values
        # If row has fewer fields than header, pad with empty strings. If more, truncate.
        row_dict = {}
        for h_idx, col_name in enumerate(header):
            val = row_values[h_idx] if h_idx < len(row_values) else ""
            row_dict[col_name] = val.strip()

        # Validate row
        is_valid, reason = validate_row(row_dict)

        if not is_valid:
            invalid_rows_info.append({
                "raw_row": raw_line if raw_line else ",".join(row_values),
                "reason": reason or "unknown validation error"
            })
            continue

        # Parse valid fields
        ticket_id = row_dict["ticket_id"]
        customer_name = row_dict["customer_name"]
        category = row_dict["category"]
        priority_raw = row_dict["priority_raw"].lower()
        priority_score = PRIORITY_MAP[priority_raw]
        created_at = datetime.strptime(row_dict["created_at"], DATE_FORMAT)
        sla_hours = int(float(row_dict["sla_hours"]))
        status = row_dict["status"].lower()

        # SLA breach check
        # breached if created_at + sla_hours < now AND status is not closed
        sla_deadline = created_at + timedelta(hours=sla_hours)
        sla_breached = (sla_deadline < now) and (status not in CLOSED_STATUSES)

        if sla_breached:
            breached_count += 1

        # Track category breakdown
        category_counts[category] = category_counts.get(category, 0) + 1

        # Create Ticket model
        ticket = Ticket(
            ticket_id=ticket_id,
            customer_name=customer_name,
            category=category,
            priority_raw=row_dict["priority_raw"],  # Preserve original casing
            priority_score=priority_score,
            created_at=created_at,
            sla_hours=sla_hours,
            status=row_dict["status"],  # Preserve original casing
            sla_breached=sla_breached,
        )
        tickets.append(ticket)

    # FR7: Check invalid-row ratio
    invalid_count = len(invalid_rows_info)
    if total_rows > 0:
        invalid_ratio = invalid_count / total_rows
        if invalid_ratio > MAX_INVALID_RATIO:
            return {}, True

    # Construct report
    report = {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "summary": {
            "total_rows": total_rows,
            "valid_tickets": len(tickets),
            "invalid_rows": invalid_count,
            "breached_count": breached_count,
            "by_category": category_counts,
        },
        "tickets": [t.to_dict() for t in tickets],
        "invalid_rows": invalid_rows_info,
    }

    return report, False
