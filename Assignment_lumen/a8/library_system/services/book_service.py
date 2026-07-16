from data.datastore import datastore


class BookService:

    def add_book(self, book):
        datastore["books"][book.id] = book

    def get_book(self, book_id):
        return datastore["books"].get(book_id)

    def update_availability(self, book_id, status):
        book = self.get_book(book_id)
        if book:
            book.is_available = status

    def delete_book(self, book_id):
        datastore["books"].pop(book_id, None)

    def list_books(self):
        return datastore["books"].values()