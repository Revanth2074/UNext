"""Command line entrypoint for the ticket processor script."""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import List

from ticket_processor.config import MAX_INVALID_RATIO
from ticket_processor.processor import process_tickets

# Configure logging format and level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ticket_processor")


def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Process NimbusTech nightly support tickets export and generate a triage report."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input CSV file containing raw tickets.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path where the output JSON report should be saved.",
    )
    return parser.parse_args()


def read_file_lines(filepath: str) -> List[str]:
    """Reads lines from a file with error handling.

    Args:
        filepath (str): Path to the file to read.

    Returns:
        List[str]: List of lines from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If there are insufficient permissions to read the file.
        Exception: For other reading errors.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Input file not found at path: '{filepath}'")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.readlines()


def main() -> None:
    """Main execution function for the ticket processor script."""
    logger.info("Starting ticket processing script.")
    args = parse_arguments()

    now = datetime.now()

    # Step 1: Read input CSV
    try:
        logger.info("Reading input CSV file from: %s", args.input)
        lines = read_file_lines(args.input)
    except FileNotFoundError as e:
        logger.error("Error reading file: %s", e)
        sys.exit(1)
    except PermissionError:
        logger.error("Permission denied reading file: %s", args.input)
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error reading input file: %s", e)
        sys.exit(1)

    logger.info("Successfully read %d raw lines (including header).", len(lines))

    # Step 2: Process tickets
    try:
        report, is_aborted = process_tickets(lines, now)
    except Exception as e:
        logger.error("Processing failed due to an unexpected error: %s", e)
        sys.exit(1)

    if is_aborted:
        logger.error(
            "Abort triggered: Invalid-row ratio exceeded threshold of %d%%. "
            "The upstream export might be corrupted.",
            int(MAX_INVALID_RATIO * 100),
        )
        sys.exit(2)

    logger.info(
        "Processing complete. Valid tickets: %d, Invalid rows skipped: %d, Breached: %d",
        report["summary"]["valid_tickets"],
        report["summary"]["invalid_rows"],
        report["summary"]["breached_count"],
    )

    if report["summary"]["invalid_rows"] > 0:
        logger.warning(
            "%d invalid rows were skipped during processing.",
            report["summary"]["invalid_rows"],
        )

    # Step 3: Write JSON report
    try:
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.exists(output_dir):
            logger.info("Creating output directory: %s", output_dir)
            os.makedirs(output_dir, exist_ok=True)

        logger.info("Writing JSON report to: %s", args.output)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        logger.info("Report written successfully.")
    except Exception as e:
        logger.error("Failed to write report to %s: %s", args.output, e)
        sys.exit(1)


if __name__ == "__main__":
    main()
