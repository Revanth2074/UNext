"""Configuration constants for the ticket processor module."""

# Priority score mapping for sorting and scoring tickets
PRIORITY_MAP = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

# The threshold ratio of invalid rows to total rows.
# If exceeded, processing is aborted.
MAX_INVALID_RATIO = 0.10

# Expected date format in the raw CSV
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Ticket statuses that are considered resolved/closed (thus not subject to SLA breach checks)
CLOSED_STATUSES = {"closed"}

# Expected columns in the input CSV
EXPECTED_COLUMNS = [
    "ticket_id",
    "customer_name",
    "category",
    "priority_raw",
    "created_at",
    "sla_hours",
    "status",
]
