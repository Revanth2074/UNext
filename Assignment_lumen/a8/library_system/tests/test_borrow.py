from models.member import Member
from models.book import Book
from models.borrow_record import BorrowRecord

from services.member_service import MemberService
from services.book_service import BookService
from services.borrow_service import BorrowService


ms = MemberService()
bs = BookService()
br = BorrowService()

member = Member(1, "Tony", 23, "Premium")
book = Book(101, "Python", "Guido", "Programming")

ms.add_member(member)
bs.add_book(book)

record = BorrowRecord(1001, member, book, "15-07-2026")

br.borrow_book(record)

assert book.is_available is False

br.return_book(1001, "20-07-2026")

assert book.is_available is True

print("Borrow Test Passed")