def validate_membership(membership_type):
    return membership_type.lower() in ["regular", "premium"]


def book_available(book):
    return book.is_available