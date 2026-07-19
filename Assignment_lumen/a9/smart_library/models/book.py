from typing import TypedDict


class Book(TypedDict):
    book_id: int
    title: str
    author: str
    publication_year: int
    category: str
    is_available: bool