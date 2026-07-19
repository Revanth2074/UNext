from typing import Sequence
from models.book import Book


def display_books(books: Sequence[Book]):

    print("\nAvailable Books")
    print("----------------")

    for book in books:
        print(f"Title : {book['title']}")
        print(f"Author: {book['author']}")
        print()