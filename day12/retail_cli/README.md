# Retail Inventory & Sales Reconciliation CLI

A modular, production-grade CLI tool built in Python to ingest, validate, and reconcile daily sales transactions against store inventory. It identifies stock issues (low stock and oversold items), flags anomalies (unknown SKUs and category mismatches), and generates both a structured JSON report and a human-readable console summary.

This project is built to satisfy the requirements of **Project 2** in the Day 12 Capstone Workbook, adhering to strict coding standards.

---

## Directory Structure

```text
retail_cli/
│
├── __init__.py          # Declares package structure
├── config.py            # Centralized settings (default low-stock threshold)
├── models.py            # Domain entities: Product and SaleTransaction classes
├── calculations.py      # Business logic: revenue, validation parsing, SKU slicing
├── io_utils.py          # Data loaders (with retry logic) and report writers
├── reporting.py         # Report compilation logic and console output presentation
├── main.py              # CLI entry point (argparse) and workflow orchestration
│
├── generate_samples.py  # Test dataset generator
└── answers.md           # Conceptual answers for Capstone Milestones 2 & 3
```

---

## Features

- **Robust Error Handling (NFR2)**: If more than 10% of rows are malformed, it logs a CRITICAL event and exits with code 1 instead of writing a partial report.
- **Resilient File Access**: Utilizes a `while` loop to retry reading files up to 3 times in case of intermittent I/O glitches.
- **central Configuration (config.py)**: Low-stock reorder thresholds are configured centrally.
- **Type Checking & Docstrings**: Every function is fully documented with PEP257-compliant docstrings and includes type hinting.
- **Product stock calculations**: Integrates `remaining_stock` methods and flags items that have been oversold.
- **Category prefix cross-check**: Uses string slicing on SKUs to verify if the SKU prefix matches the product's declared category.

---

## How to Run

### Step 1: Generate Test Datasets
You can generate a test inventory file (`inventory.json`), a valid transactions file (`sales.csv`), and a corrupt transactions file (`sales_corrupt.csv`) by running:

```bash
python -m retail_cli.generate_samples
```

### Step 2: Run Reconcile (Valid Sales Batch)
To run the reconciliation tool on a valid sales batch:

```bash
python -m retail_cli.main --inventory retail_cli/inventory.json --sales retail_cli/sales.csv --output retail_cli/report.json --reorder-threshold 10
```

This will output a console summary and write `retail_cli/report.json`.

### Step 3: Run Reconcile (Corrupt Sales Batch - NFR2 Test)
To verify the system flags when more than 10% of rows are corrupt:

```bash
python -m retail_cli.main --inventory retail_cli/inventory.json --sales retail_cli/sales_corrupt.csv --output retail_cli/report.json
```

This will log a `CRITICAL` error and exit with status code 1.
