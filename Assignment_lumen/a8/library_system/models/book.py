class Book:

    def __init__(self, book_id, title, author, genre):
        self.id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.title} by {self.author} ({self.genre}) - {status}"