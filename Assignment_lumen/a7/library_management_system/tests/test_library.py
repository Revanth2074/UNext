import unittest
import os

from services.library_service import (
    add_book,
    register_member,
    borrow_book,
    return_book
)

from utils.file_handler import (
    read_books,
    read_members,
    write_books,
    write_members
)

from exceptions.custom_exceptions import (
    BookNotFoundError,
    MemberNotFoundError,
    BookAlreadyBorrowedError,
    BookNotBorrowedError
)


class TestLibraryManagementSystem(unittest.TestCase):

    def setUp(self):

        # Reset test data before every test
        write_books([
            [
                "101",
                "Python Programming",
                "John Smith",
                "Programming",
                "Available"
            ],
            [
                "102",
                "Data Science Handbook",
                "Jane Miller",
                "Data Science",
                "Available"
            ]
        ])

        write_members([
            [
                "M001",
                "Ravi",
                "ravi@gmail.com",
                ""
            ]
        ])


    # TC01 View Books
    def test_view_books(self):

        books = read_books()

        self.assertEqual(len(books), 2)
        self.assertEqual(
            books[0][1],
            "Python Programming"
        )


    # TC02 Add New Book
    def test_add_book(self):

        add_book(
            "103",
            "Machine Learning",
            "Andrew Ng",
            "AI"
        )

        books = read_books()

        self.assertEqual(len(books), 3)


    # TC03 Register Member
    def test_register_member(self):

        register_member(
            "M002",
            "Asha",
            "asha@gmail.com"
        )

        members = read_members()

        self.assertEqual(len(members), 2)


    # TC04 Borrow Available Book
    def test_borrow_book(self):

        borrow_book(
            "M001",
            "101"
        )

        books = read_books()

        self.assertEqual(
            books[0][4],
            "Borrowed"
        )


    # TC05 Borrow Already Borrowed Book
    def test_borrow_already_borrowed_book(self):

        borrow_book(
            "M001",
            "101"
        )

        with self.assertRaises(
            BookAlreadyBorrowedError
        ):
            borrow_book(
                "M001",
                "101"
            )


    # TC06 Invalid Book ID
    def test_invalid_book(self):

        with self.assertRaises(
            BookNotFoundError
        ):
            borrow_book(
                "M001",
                "999"
            )


    # TC07 Invalid Member ID
    def test_invalid_member(self):

        with self.assertRaises(
            MemberNotFoundError
        ):
            borrow_book(
                "M999",
                "101"
            )


    # TC08 Return Borrowed Book
    def test_return_book(self):

        borrow_book(
            "M001",
            "101"
        )

        return_book(
            "M001",
            "101"
        )

        books = read_books()

        self.assertEqual(
            books[0][4],
            "Available"
        )


    # TC09 Return Book Not Borrowed
    def test_return_wrong_book(self):

        with self.assertRaises(
            BookNotBorrowedError
        ):
            return_book(
                "M001",
                "101"
            )


if __name__ == "__main__":
    unittest.main()