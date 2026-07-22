"""
Models module.

Defines the domain classes representing products in the inventory
and individual sales transactions.
"""

class Product:
    """
    Represents a product item in the store's inventory.

    Attributes:
        sku: Unique stock keeping unit string.
        name: Name of the product.
        unit_price: Price per single unit.
        stock_qty: Available quantity in stock.
        category: Category of the product (e.g., Electronics, Clothing).
    """

    def __init__(
        self,
        sku: str,
        name: str,
        unit_price: float,
        stock_qty: int,
        category: str
    ) -> None:
        """Initializes a new Product instance."""
        self.sku = sku
        self.name = name
        self.unit_price = unit_price
        self.stock_qty = stock_qty
        self.category = category

    def remaining_stock(self, qty_sold: int) -> int:
        """
        Computes the remaining stock after a quantity has been sold.

        Args:
            qty_sold: The total quantity sold across transactions.

        Returns:
            The remaining stock quantity (can be negative if oversold).
        """
        return self.stock_qty - qty_sold


class SaleTransaction:
    """
    Represents a single sales transaction record.

    Attributes:
        sku: Stock keeping unit for the item sold.
        qty_sold: Number of units sold.
        discount_pct: Applied discount percentage (0 to 100).
        channel: Sales channel ('online' or 'in-store').
    """

    def __init__(
        self,
        sku: str,
        qty_sold: int,
        discount_pct: float,
        channel: str
    ) -> None:
        """Initializes a new SaleTransaction instance."""
        self.sku = sku
        self.qty_sold = qty_sold
        self.discount_pct = discount_pct
        self.channel = channel

    def line_revenue(self, product: Product) -> float:
        """
        Computes the line revenue for this transaction given the product info.

        Formula: qty_sold * unit_price * (1 - discount_pct / 100), rounded to 2 d.p.
        Clamps discount_pct to [0, 100] as a safety measure.

        Args:
            product: The Product instance matching this transaction's SKU.

        Returns:
            The calculated revenue for the transaction, rounded to 2 decimal places.

        Raises:
            ValueError: If the product SKU does not match the transaction SKU.
        """
        if product.sku != self.sku:
            raise ValueError(
                f"Product SKU mismatch: transaction has {self.sku}, product has {product.sku}"
            )
        
        # Clamp discount_pct to 0-100
        clamped_discount = max(0.0, min(100.0, self.discount_pct))
        
        revenue = self.qty_sold * product.unit_price * (1.0 - clamped_discount / 100.0)
        return round(revenue, 2)
