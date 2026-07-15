class OutOfStockError(Exception):
    """Raised when product quantity is unavailable."""
    pass


class ProductNotFoundError(Exception):
    """Raised when product does not exist."""
    pass


class EmptyCartError(Exception):
    """Raised when checkout is attempted with empty cart."""
    pass