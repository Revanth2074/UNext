class Member:
    def __init__(self, member_id, name, email, borrowed_books=""):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_books = borrowed_books

    def to_list(self):
        return [
            self.member_id,
            self.name,
            self.email,
            self.borrowed_books
        ]

    def __str__(self):
        return (f"Member ID : {self.member_id}\n"
                f"Name      : {self.name}\n"
                f"Email     : {self.email}\n"
                f"Borrowed Books : {self.borrowed_books}")