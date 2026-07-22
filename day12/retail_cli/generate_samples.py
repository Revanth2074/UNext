"""
Sample Data Generator.

Generates testing datasets including `inventory.json`, `sales.csv` (normal),
and `sales_corrupt.csv` (corrupt) to verify the behavior of the reconciliation tool.
"""

import json
import os

def generate_samples(target_dir: str) -> None:
    # 1. Define inventory
    inventory = [
        {
            "sku": "SKU-ELEC1001",
            "name": "Wireless Mouse",
            "unit_price": 25.99,
            "stock_qty": 50,
            "category": "Electronics"
        },
        {
            "sku": "SKU-ELEC1002",
            "name": "Mechanical Keyboard",
            "unit_price": 89.99,
            "stock_qty": 5,
            "category": "Electronics"
        },
        {
            "sku": "SKU-CLOT2001",
            "name": "Cotton T-Shirt",
            "unit_price": 19.99,
            "stock_qty": 100,
            "category": "Clothing"
        },
        {
            "sku": "SKU-CLOT2002",
            "name": "Denim Jeans",
            "unit_price": 49.99,
            "stock_qty": 8, # Low stock naturally (remaining 8 < threshold 10)
            "category": "Clothing"
        },
        {
            "sku": "SKU-TOYS4001",
            "name": "Action Figure",
            "unit_price": 14.99,
            "stock_qty": 50,
            "category": "Electronics" # Intentional category mismatch (TOYS vs Electronics)
        }
    ]

    # Write inventory.json
    inv_path = os.path.join(target_dir, "inventory.json")
    with open(inv_path, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=4)
    print(f"Generated sample inventory: {inv_path}")

    # 2. Define sales (valid path, 1 malformed row out of 11 = 9.09% < 10% limit)
    # Anomalies included:
    # - SKU-ELEC1002 total sold is 6 (stock is 5, so it becomes oversold)
    # - SKU-TOYS3001 is unknown SKU
    # - Row 5 is malformed (invalid discount_pct)
    # - SKU-CLOT2002 is not sold, remaining stock is 8, so it stays low-stock
    # - SKU-ELEC1001 remaining stock will fall to: 50 - 2 - 4 - 1 - 1 = 42
    # - SKU-TOYS4001 has category mismatch in inventory (TOYS prefix, Electronics category)
    sales_rows = [
        "sku,qty_sold,discount_pct,channel",
        "SKU-ELEC1001,2,10.0,online",
        "SKU-ELEC1002,6,0.0,in-store",
        "SKU-CLOT2001,5,15.0,online",
        "SKU-TOYS3001,3,0.0,online",  # Unknown SKU
        "SKU-ELEC1001,3,invalid_discount,online",  # Malformed row
        "SKU-CLOT2001,4,20.0,in-store",
        "SKU-ELEC1001,1,0.0,online",
        "SKU-CLOT2001,2,5.0,online",
        "SKU-ELEC1001,1,0.0,in-store",
        "SKU-CLOT2001,1,0.0,online",
        "SKU-TOYS4001,1,10.0,in-store"  # Category mismatch SKU
    ]

    sales_path = os.path.join(target_dir, "sales.csv")
    with open(sales_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sales_rows) + "\n")
    print(f"Generated sample sales (normal): {sales_path}")

    # 3. Define corrupt sales (fails NFR2 check, 2 malformed rows out of 6 total = 33.3% > 10%)
    corrupt_sales_rows = [
        "sku,qty_sold,discount_pct,channel",
        "SKU-ELEC1001,2,10.0,online",
        "SKU-ELEC1002,1,0.0,in-store",
        "SKU-CLOT2001,invalid_qty,15.0,online",  # Malformed row 1
        "SKU-CLOT2001,4,20.0,in-store",
        "SKU-ELEC1001,1,invalid_discount,online",  # Malformed row 2
        "SKU-CLOT2001,1,0.0,online"
    ]

    corrupt_sales_path = os.path.join(target_dir, "sales_corrupt.csv")
    with open(corrupt_sales_path, "w", encoding="utf-8") as f:
        f.write("\n".join(corrupt_sales_rows) + "\n")
    print(f"Generated sample corrupt sales (for NFR2 test): {corrupt_sales_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generate_samples(current_dir)
