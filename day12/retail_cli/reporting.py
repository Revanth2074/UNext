"""
Reporting module.

Builds the daily reconciliation report by aggregating revenues,
determining oversold and low-stock SKUs, identifying anomalies,
and printing the human-readable console summary.
"""

import logging
from typing import Dict, List, Set, Tuple
from datetime import datetime
from .models import Product, SaleTransaction
from .calculations import category_code_from_sku

logger = logging.getLogger(__name__)


def build_report(
    inventory: Dict[str, Product],
    transactions: List[SaleTransaction],
    reorder_threshold: int,
    malformed_count: int,
    total_count: int
) -> Tuple[dict, Set[str], Set[str], Set[str]]:
    """
    Orchestrates the business rules to construct a structured reconciliation report.

    Args:
        inventory: Dictionary of SKU to Product instances.
        transactions: List of valid SaleTransaction instances.
        reorder_threshold: Threshold below which a product is considered low-stock.
        malformed_count: Count of malformed CSV rows.
        total_count: Total count of CSV rows processed.

    Returns:
        A tuple of:
            - The complete report dictionary.
            - Set of low-stock SKUs.
            - Set of oversold SKUs.
            - Set of unknown SKUs.
    """
    total_revenue = 0.0
    revenue_by_category: Dict[str, float] = {}
    revenue_by_channel: Dict[str, float] = {"online": 0.0, "in-store": 0.0}
    
    qty_sold_per_sku: Dict[str, int] = {}
    unknown_skus: Set[str] = set()
    category_mismatches: List[dict] = []

    # Process transactions
    for tx in transactions:
        if tx.sku not in inventory:
            unknown_skus.add(tx.sku)
            logger.warning(f"Anomaly: Transaction contains SKU '{tx.sku}' which is not in inventory.")
            continue

        product = inventory[tx.sku]
        try:
            line_rev = tx.line_revenue(product)
            total_revenue += line_rev
            
            # Aggregate channel revenue
            revenue_by_channel[tx.channel] = revenue_by_channel.get(tx.channel, 0.0) + line_rev
            
            # Aggregate category revenue
            revenue_by_category[product.category] = revenue_by_category.get(product.category, 0.0) + line_rev
            
            # Track sales quantity
            qty_sold_per_sku[tx.sku] = qty_sold_per_sku.get(tx.sku, 0) + tx.qty_sold
        except ValueError as e:
            logger.error(f"Error computing line revenue for transaction: {e}")

    # Track stock alerts and cross-checks
    oversold_skus: Set[str] = set()
    low_stock_skus: Set[str] = set()
    oversold_details: List[dict] = []
    
    for sku, product in inventory.items():
        qty_sold = qty_sold_per_sku.get(sku, 0)
        remaining = product.remaining_stock(qty_sold)
        
        # Check if SKU is oversold (qty_sold > stock_qty)
        if qty_sold > product.stock_qty:
            oversold_skus.add(sku)
            oversold_details.append({
                "sku": sku,
                "name": product.name,
                "stock_qty": product.stock_qty,
                "qty_sold": qty_sold,
                "oversold_by": qty_sold - product.stock_qty
            })
            logger.warning(
                f"Alert: SKU '{sku}' ({product.name}) is oversold. "
                f"Stock: {product.stock_qty}, Sold: {qty_sold}."
            )

        # Check if remaining stock is low-stock (< reorder_threshold)
        if remaining < reorder_threshold:
            low_stock_skus.add(sku)
            logger.info(
                f"Reorder alert: SKU '{sku}' ({product.name}) has low stock. "
                f"Remaining: {remaining} (threshold: {reorder_threshold})."
            )

        # Cross-check SKU category code against declared category (Milestone 2 Q2.5)
        try:
            cat_code = category_code_from_sku(sku)
            # e.g., ELEC code should match 'Electronics' (case insensitive match)
            if not product.category.upper().startswith(cat_code):
                msg = f"SKU prefix '{cat_code}' does not match category '{product.category}'"
                logger.warning(f"Category mismatch for SKU '{sku}': {msg}")
                category_mismatches.append({
                    "sku": sku,
                    "declared_category": product.category,
                    "sku_code": cat_code
                })
        except ValueError as e:
            logger.warning(f"Could not cross-check SKU '{sku}': {e}")

    # Round all aggregates to 2 decimal places (NFR4)
    total_revenue = round(total_revenue, 2)
    for cat in revenue_by_category:
        revenue_by_category[cat] = round(revenue_by_category[cat], 2)
    for ch in revenue_by_channel:
        revenue_by_channel[ch] = round(revenue_by_channel[ch], 2)

    # Build report dict
    report = {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "reorder_threshold": reorder_threshold
        },
        "file_summary": {
            "total_rows_processed": total_count,
            "valid_rows": len(transactions),
            "malformed_rows": malformed_count,
            "malformed_ratio": round(malformed_count / total_count, 4) if total_count > 0 else 0.0
        },
        "financial_summary": {
            "total_revenue": total_revenue,
            "revenue_by_category": revenue_by_category,
            "revenue_by_channel": revenue_by_channel
        },
        "stock_alerts": {
            "oversold_skus": oversold_details,
            "low_stock_skus": list(low_stock_skus)
        },
        "anomalies": {
            "unknown_skus_sold": list(unknown_skus),
            "category_mismatches": category_mismatches
        }
    }

    return report, low_stock_skus, oversold_skus, unknown_skus


def print_console_summary(report: dict) -> None:
    """
    Prints a beautiful, human-readable summary of the reconciliation report to the console.

    Args:
        report: The reconciliation report dictionary.
    """
    print("=" * 60)
    print("        RETAIL INVENTORY & SALES RECONCILIATION SUMMARY")
    print("=" * 60)
    
    meta = report["report_metadata"]
    print(f"Generated At:      {meta['generated_at']}")
    print(f"Reorder Threshold: {meta['reorder_threshold']} units")
    print("-" * 60)
    
    fs = report["file_summary"]
    print(f"Total Rows Ingested:   {fs['total_rows_processed']}")
    print(f"Valid Rows Parsed:     {fs['valid_rows']}")
    print(f"Malformed Rows Skipped: {fs['malformed_rows']} ({fs['malformed_ratio'] * 100:.1f}%)")
    print("-" * 60)
    
    fin = report["financial_summary"]
    print(f"TOTAL REVENUE:         ${fin['total_revenue']:.2f}")
    print("\nRevenue by Category:")
    for cat, rev in fin["revenue_by_category"].items():
        print(f"  - {cat:<18} : ${rev:.2f}")
        
    print("\nRevenue by Channel:")
    for ch, rev in fin["revenue_by_channel"].items():
        print(f"  - {ch.capitalize():<18} : ${rev:.2f}")
    print("-" * 60)
    
    alerts = report["stock_alerts"]
    print(f"Oversold SKUs:         {len(alerts['oversold_skus'])}")
    for item in alerts["oversold_skus"]:
        print(f"  [ALERT] SKU: {item['sku']} ({item['name']}) | Stock: {item['stock_qty']} | Sold: {item['qty_sold']} | Oversold By: {item['oversold_by']}")
        
    print(f"Low-Stock SKUs:        {len(alerts['low_stock_skus'])}")
    if alerts["low_stock_skus"]:
        print(f"  reorder required: {', '.join(alerts['low_stock_skus'])}")
        
    anom = report["anomalies"]
    print(f"Unknown SKUs Sold:     {len(anom['unknown_skus_sold'])}")
    if anom["unknown_skus_sold"]:
        print(f"  [ERROR] Unknown SKU Alerts: {', '.join(anom['unknown_skus_sold'])}")
        
    print(f"Category Mismatches:   {len(anom['category_mismatches'])}")
    for item in anom["category_mismatches"]:
        print(f"  [WARNING] SKU: {item['sku']} | Code: {item['sku_code']} | Declared: {item['declared_category']}")
    print("=" * 60)
