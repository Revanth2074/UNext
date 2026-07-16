from models.member import Member
from models.book import Book
from models.borrow_record import BorrowRecord

from services.library_system import LibrarySystem


library = LibrarySystem()

# Add Member
member = Member(
    1,
    "Tony Stark",
    24,
    "Premium"
)

library.member_service.add_member(member)

# Add Books
book1 = Book(
    101,
    "Python Programming",
    "Guido van Rossum",
    "Programming"
)

book2 = Book(
    102,
    "Data Structures",
    "Mark Allen",
    "Education"
)

library.book_service.add_book(book1)
library.book_service.add_book(book2)

# Borrow Book
record = BorrowRecord(
    1001,
    member,
    book1,
    "16-07-2026"
)

library.borrow_service.borrow_book(record)

print("\nMembers")
for m in library.member_service.list_members():
    print(m)

print("\nBooks")
for b in library.book_service.list_books():
    print(b)

print("\nBorrow Records")
for r in library.borrow_service.list_records():
    print(r)

# Return Book
library.borrow_service.return_book(
    1001,
    "20-07-2026"
)

print("\nAfter Returning")

for b in library.book_service.list_books():
    print(b)