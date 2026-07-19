from models.book import Book

from services.member_service import display_member

from services.book_service import display_books

from services.notification_service import (
    notify_member,
    email_notification,
    sms_notification,
    whatsapp_notification
)


# -------------------------------
# Part 1 : TypedDict
# -------------------------------

book1: Book = {
    "book_id": 101,
    "title": "Python Programming",
    "author": "Guido van Rossum",
    "publication_year": 2024,
    "category": "Programming",
    "is_available": True
}

book2: Book = {
    "book_id": 102,
    "title": "Data Structures",
    "author": "Mark Allen",
    "publication_year": 2023,
    "category": "Education",
    "is_available": True
}


# -------------------------------
# Part 2 : Union
# -------------------------------

display_member(1001, "Tony Stark")

display_member("STU-4501", "Peter Parker")


# -------------------------------
# Part 3 : Sequence
# -------------------------------

book_list = [book1, book2]

book_tuple = (book1, book2)

display_books(book_list)

display_books(book_tuple)


# -------------------------------
# Part 4 : Callable
# -------------------------------

notify_member(
    "Tony Stark",
    "Your book has been issued successfully.",
    email_notification
)

notify_member(
    "Peter Parker",
    "Please return your book tomorrow.",
    sms_notification
)

notify_member(
    "Bruce Banner",
    "Your reserved book is available.",
    whatsapp_notification
)