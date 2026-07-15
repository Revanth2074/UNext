class Book:
    def __init__(self, book_id, title, author, category, status="Available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.status = status

    def to_list(self):
        return [
            self.book_id,
            self.title,
            self.author,
            self.category,
            self.status
        ]

    def __str__(self):
        return (f"Book ID : {self.book_id}\n"
                f"Title   : {self.title}\n"
                f"Author  : {self.author}\n"
                f"Category: {self.category}\n"
                f"Status  : {self.status}")