"""
Calculations module.

Contains pure functions for parsing, validating, and performing
financial and inventory calculations.
"""

def parse_sale_row(row: dict) -> dict:
    """
    Validates a raw CSV row dictionary representing a sales transaction
    and casts fields to their correct types.

    Required fields in row:
        - sku: non-empty string
        - qty_sold: integer >= 0
        - discount_pct: float between 0.0 and 100.0 (clamped if out of range in compute_revenue)
        - channel: 'online' or 'in-store'

    Args:
        row: A dictionary containing string values from the CSV.

    Returns:
        A dictionary with cleaned and cast values.

    Raises:
        ValueError: If any field is missing, invalid, or cannot be cast.
    """
    # Check for missing keys
    required_fields = ["sku", "qty_sold", "discount_pct", "channel"]
    for field in required_fields:
        if field not in row or row[field] is None:
            raise ValueError(f"Missing required field: '{field}'")

    sku = row["sku"].strip()
    if not sku:
        raise ValueError("SKU field is empty")

    raw_qty = row["qty_sold"].strip()
    try:
        qty_sold = int(raw_qty)
    except ValueError as e:
        raise ValueError(f"Invalid quantity '{raw_qty}': must be an integer") from e

    if qty_sold < 0:
        raise ValueError(f"Invalid quantity {qty_sold}: cannot be negative")

    raw_discount = row["discount_pct"].strip()
    try:
        discount_pct = float(raw_discount)
    except ValueError as e:
        raise ValueError(f"Invalid discount '{raw_discount}': must be a float") from e

    channel = row["channel"].strip().lower()
    if channel not in ["online", "in-store"]:
        raise ValueError(f"Invalid sales channel '{channel}': must be 'online' or 'in-store'")

    return {
        "sku": sku,
        "qty_sold": qty_sold,
        "discount_pct": discount_pct,
        "channel": channel
    }


def compute_revenue(unit_price: float, qty_sold: int, discount_pct: float) -> float:
    """
    Computes line revenue with discount clamping using conditional flow.

    If discount_pct is outside [0.0, 100.0], it is clamped.

    Args:
        unit_price: Price per single unit.
        qty_sold: Number of units sold.
        discount_pct: Applied discount percentage.

    Returns:
        Calculated revenue rounded to 2 decimal places.
    """
    if discount_pct < 0.0:
        clamped_discount = 0.0
    elif discount_pct > 100.0:
        clamped_discount = 100.0
    else:
        clamped_discount = discount_pct

    revenue = qty_sold * unit_price * (1.0 - clamped_discount / 100.0)
    return round(revenue, 2)


def category_code_from_sku(sku: str) -> str:
    """
    Extracts the category code from a SKU string using slicing.
    Format assumed: 'SKU-<category_code><number>' (e.g. 'SKU-ELEC1001' -> 'ELEC')

    Args:
        sku: The SKU string to process.

    Returns:
        The extracted category code in uppercase.

    Raises:
        ValueError: If SKU format is invalid.
    """
    if not sku.startswith("SKU-"):
        raise ValueError(f"Invalid SKU prefix in '{sku}': must start with 'SKU-'")
    
    # Strip the prefix 'SKU-'
    remainder = sku[4:]
    
    # Find the boundary where numbers start
    boundary = 0
    while boundary < len(remainder) and not remainder[boundary].isdigit():
        boundary += 1
        
    if boundary == 0:
        raise ValueError(f"No category code found in SKU '{sku}'")
        
    return remainder[:boundary].upper()
