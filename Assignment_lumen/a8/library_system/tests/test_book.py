from models.book import Book
from services.book_service import BookService


service = BookService()

book = Book(101, "Python", "Guido", "Programming")

service.add_book(book)

assert service.get_book(101).title == "Python"

service.update_availability(101, False)

assert service.get_book(101).is_available is False

service.delete_book(101)

assert service.get_book(101) is None

print("Book Test Passed")