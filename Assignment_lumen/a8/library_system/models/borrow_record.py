class BorrowRecord:

    def __init__(self, borrow_id, member, book, borrow_date, return_date=None):
        self.id = borrow_id
        self.member = member
        self.book = book
        self.borrow_date = borrow_date
        self.return_date = return_date

    def __str__(self):
        return (
            f"Borrow ID:{self.id}\n"
            f"Member:{self.member.name}\n"
            f"Book:{self.book.title}\n"
            f"Borrow Date:{self.borrow_date}\n"
            f"Return Date:{self.return_date}"
        )