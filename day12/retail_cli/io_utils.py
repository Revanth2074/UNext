"""
I/O utilities module.

Handles reading product inventory from JSON and daily sales from CSV,
including flaky-read retries, malformed row detection, and writing the JSON report.
"""

import csv
import json
import logging
import time
from typing import Dict, List, Tuple
from .models import Product, SaleTransaction
from .calculations import parse_sale_row

logger = logging.getLogger(__name__)


def load_inventory(json_path: str) -> Dict[str, Product]:
    """
    Loads product inventory from a JSON file.
    Implements a resilient retry loop (up to 3 attempts) for flaky reads.

    Args:
        json_path: File path to the inventory JSON file.

    Returns:
        A dictionary mapping SKU strings to Product instances.

    Raises:
        FileNotFoundError: If the file does not exist after retries.
        json.JSONDecodeError: If the JSON file is malformed.
        Exception: For other OS errors.
    """
    attempts = 0
    max_attempts = 3
    last_exception = None

    while attempts < max_attempts:
        attempts += 1
        logger.info(f"Attempt {attempts}: Loading inventory from {json_path}")
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Expecting a list of product dicts
            inventory: Dict[str, Product] = {}
            for item in data:
                # Basic validation of keys in JSON
                sku = item["sku"].strip()
                name = item["name"].strip()
                unit_price = float(item["unit_price"])
                stock_qty = int(item["stock_qty"])
                category = item["category"].strip()
                
                inventory[sku] = Product(
                    sku=sku,
                    name=name,
                    unit_price=unit_price,
                    stock_qty=stock_qty,
                    category=category
                )
            logger.info(f"Successfully loaded {len(inventory)} products from inventory.")
            return inventory
        except (IOError, OSError) as e:
            logger.warning(f"IOError on attempt {attempts} reading {json_path}: {e}")
            last_exception = e
            if attempts < max_attempts:
                time.sleep(0.1)  # small pause before retry
        except Exception as e:
            logger.error(f"Fatal error reading inventory {json_path}: {e}")
            raise

    logger.critical(f"All {max_attempts} attempts to read {json_path} failed.")
    if last_exception:
        raise last_exception
    raise RuntimeError(f"Failed to read inventory {json_path}")


def load_sales(csv_path: str) -> Tuple[List[SaleTransaction], int, int]:
    """
    Loads sales transactions from a CSV file using csv.DictReader.
    Applies parse_sale_row inside a try/except ValueError to count and skip malformed rows.
    Implements a resilient retry loop (up to 3 attempts) for flaky reads.

    Args:
        csv_path: File path to the sales CSV file.

    Returns:
        A tuple of:
            - List of valid SaleTransaction instances.
            - Count of malformed rows.
            - Total number of rows parsed (excluding header).

    Raises:
        FileNotFoundError: If the file does not exist after retries.
        Exception: For other OS errors.
    """
    attempts = 0
    max_attempts = 3
    last_exception = None
    raw_rows: List[dict] = []

    # Flaky read simulation retry loop for opening & reading file
    while attempts < max_attempts:
        attempts += 1
        logger.info(f"Attempt {attempts}: Reading sales file {csv_path}")
        try:
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                # Field names validation
                if not reader.fieldnames:
                    raise ValueError("CSV file is empty or missing headers")
                
                # Consume file into memory to ensure read was fully successful
                raw_rows = list(reader)
            break
        except (IOError, OSError) as e:
            logger.warning(f"IOError on attempt {attempts} reading {csv_path}: {e}")
            last_exception = e
            if attempts < max_attempts:
                time.sleep(0.1)
        except Exception as e:
            logger.error(f"Fatal error reading sales {csv_path}: {e}")
            raise
    else:
        logger.critical(f"All {max_attempts} attempts to read {csv_path} failed.")
        if last_exception:
            raise last_exception
        raise RuntimeError(f"Failed to read sales {csv_path}")

    # Parse individual rows
    transactions: List[SaleTransaction] = []
    malformed_count = 0
    total_count = 0

    for idx, row in enumerate(raw_rows, start=1):
        total_count += 1
        try:
            cleaned_row = parse_sale_row(row)
            transaction = SaleTransaction(
                sku=cleaned_row["sku"],
                qty_sold=cleaned_row["qty_sold"],
                discount_pct=cleaned_row["discount_pct"],
                channel=cleaned_row["channel"]
            )
            transactions.append(transaction)
        except ValueError as e:
            logger.warning(f"Malformed row skipped at line {idx}: {e}")
            malformed_count += 1

    logger.info(f"Sales file processing summary: {len(transactions)} valid rows, {malformed_count} malformed rows, {total_count} total rows.")
    return transactions, malformed_count, total_count


def write_report(report: dict, output_path: str) -> None:
    """
    Writes the daily reconciliation report to a file in indented JSON format.

    Args:
        report: The reconciliation report dictionary.
        output_path: File path to write the report to.
    """
    logger.info(f"Writing reconciliation report to {output_path}")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
        logger.info("Report written successfully.")
    except (IOError, OSError) as e:
        logger.error(f"Failed to write report to {output_path}: {e}")
        raise
