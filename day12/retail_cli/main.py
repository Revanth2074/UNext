"""
Main execution module.

Orchestrates the retail reconciliation CLI pipeline: configures logging,
parses command-line arguments, prints the startup banner, loads inputs,
performs validation checks, runs reporting, and writes files.
"""

import argparse
import sys
import logging
from datetime import date
from .config import DEFAULT_REORDER_THRESHOLD
from .io_utils import load_inventory, load_sales, write_report
from .reporting import build_report, print_console_summary

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("retail_cli")


def run_pipeline(
    inventory_path: str,
    sales_path: str,
    output_path: str,
    reorder_threshold: int
) -> None:
    """
    Runs the full ingestion, validation, and reporting pipeline.

    Args:
        inventory_path: Path to the inventory JSON file.
        sales_path: Path to the sales CSV file.
        output_path: Path where the output JSON report will be written.
        reorder_threshold: The low-stock threshold limit.
    """
    logger.info("Initializing Retail Reconciliation Pipeline...")

    # Load inventory
    try:
        inventory = load_inventory(inventory_path)
    except FileNotFoundError:
        logger.error(f"Inventory file not found: {inventory_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to load inventory: {e}")
        sys.exit(1)

    # Load sales
    try:
        transactions, malformed_count, total_count = load_sales(sales_path)
    except FileNotFoundError:
        logger.error(f"Sales file not found: {sales_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to load sales: {e}")
        sys.exit(1)

    # Check for empty file
    if total_count == 0:
        logger.error("No transactions found in sales file to process.")
        sys.exit(1)

    # NFR2 Check: If >10% of sales rows are malformed, log CRITICAL and exit
    malformed_ratio = malformed_count / total_count
    if malformed_ratio > 0.10:
        logger.critical(
            f"CRITICAL: Batch failed due to excessive malformed data. "
            f"Malformed rows: {malformed_count}/{total_count} ({malformed_ratio * 100:.2f}%). "
            f"Limit is 10%."
        )
        sys.exit(1)

    # Build the report
    report, low_stock, oversold, unknown = build_report(
        inventory=inventory,
        transactions=transactions,
        reorder_threshold=reorder_threshold,
        malformed_count=malformed_count,
        total_count=total_count
    )

    # Write the report JSON
    try:
        write_report(report, output_path)
    except Exception as e:
        logger.error(f"Failed to write report to file: {e}")
        sys.exit(1)

    # Print final console summary (the only place where print is used)
    print_console_summary(report)


def main() -> None:
    """Parses command-line arguments and runs the pipeline."""
    parser = argparse.ArgumentParser(
        description="Retail Inventory & Sales Reconciliation CLI Tool"
    )
    parser.add_argument(
        "--inventory",
        required=True,
        help="Path to the product inventory JSON file"
    )
    parser.add_argument(
        "--sales",
        required=True,
        help="Path to the sales transactions CSV file"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to save the output JSON report"
    )
    parser.add_argument(
        "--reorder-threshold",
        type=int,
        default=DEFAULT_REORDER_THRESHOLD,
        help=f"Minimum stock threshold for reorder alerts (default: {DEFAULT_REORDER_THRESHOLD})"
    )

    args = parser.parse_args()
    run_pipeline(
        inventory_path=args.inventory,
        sales_path=args.sales,
        output_path=args.output,
        reorder_threshold=args.reorder_threshold
    )


if __name__ == "__main__":
    # Startup banner (Milestone 1 Q1.1)
    # This block executes only when this file is run directly.
    today_str = date.today().strftime("%B %d, %Y")
    banner = f"""
============================================================
              NORTHFIELD RETAIL CO. RECONCILIATION
                  System Date: {today_str}
============================================================
"""
    print(banner)
    main()
