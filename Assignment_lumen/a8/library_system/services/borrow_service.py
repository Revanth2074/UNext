from data.datastore import datastore


class BorrowService:

    def borrow_book(self, record):
        if record.book.is_available:
            record.book.is_available = False
            datastore["borrows"][record.id] = record
            print("Book Borrowed Successfully")
        else:
            print("Book Not Available")

    def return_book(self, borrow_id, return_date):
        record = datastore["borrows"].get(borrow_id)

        if record:
            record.return_date = return_date
            record.book.is_available = True
            print("Book Returned Successfully")

    def delete_record(self, borrow_id):
        datastore["borrows"].pop(borrow_id, None)

    def get_record(self, borrow_id):
        return datastore["borrows"].get(borrow_id)

    def list_records(self):
        return datastore["borrows"].values()