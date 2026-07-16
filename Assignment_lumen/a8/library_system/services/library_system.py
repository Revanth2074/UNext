from services.member_service import MemberService
from services.book_service import BookService
from services.borrow_service import BorrowService


class LibrarySystem:

    def __init__(self):
        self.member_service = MemberService()
        self.book_service = BookService()
        self.borrow_service = BorrowService()