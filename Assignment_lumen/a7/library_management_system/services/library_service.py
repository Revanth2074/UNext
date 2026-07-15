from models.book import Book
from models.member import Member
from utils.file_handler import (
    read_books,
    write_books,
    read_members,
    write_members
)

from exceptions.custom_exceptions import (
    BookNotFoundError,
    MemberNotFoundError,
    BookAlreadyBorrowedError,
    BookNotBorrowedError
)


# -----------------------------
# View Books
# -----------------------------
def view_books():
    books = read_books()

    print("\n========== Available Books ==========\n")

    for book in books:
        print(f"Book ID : {book[0]}")
        print(f"Title   : {book[1]}")
        print(f"Author  : {book[2]}")
        print(f"Category: {book[3]}")
        print(f"Status  : {book[4]}")
        print("-" * 35)


# -----------------------------
# Add Book
# -----------------------------
def add_book(book_id, title, author, category):

    books = read_books()

    new_book = Book(
        book_id,
        title,
        author,
        category,
        "Available"
    )

    books.append(new_book.to_list())

    write_books(books)

    print("Book added successfully.")


# -----------------------------
# Register Member
# -----------------------------
def register_member(member_id, name, email):

    members = read_members()

    new_member = Member(
        member_id,
        name,
        email,
        ""
    )

    members.append(new_member.to_list())

    write_members(members)

    print("Member registered successfully.")


# -----------------------------
# Borrow Book
# -----------------------------
def borrow_book(member_id, book_id):

    books = read_books()
    members = read_members()

    member_found = False
    book_found = False

    # Check Member
    for member in members:
        if member[0] == member_id:
            member_found = True
            member_record = member
            break

    if not member_found:
        raise MemberNotFoundError("Error: Member not found.")

    # Check Book
    for book in books:

        if book[0] == book_id:

            book_found = True

            if book[4] == "Borrowed":
                raise BookAlreadyBorrowedError(
                    "Error: Book is already borrowed."
                )

            # Update Book Status
            book[4] = "Borrowed"

            # Update Member Borrowed Books
            if member_record[3] == "":
                member_record[3] = book_id
            else:
                member_record[3] += "," + book_id

            break

    if not book_found:
        raise BookNotFoundError("Error: Book not found.")

    write_books(books)
    write_members(members)

    print("Book borrowed successfully.")


# -----------------------------
# Return Book
# -----------------------------
def return_book(member_id, book_id):

    books = read_books()
    members = read_members()

    member_found = False
    book_found = False

    # Find Member
    for member in members:

        if member[0] == member_id:

            member_found = True

            borrowed = member[3].split(",") if member[3] else []

            if book_id not in borrowed:
                raise BookNotBorrowedError(
                    "Error: Book not borrowed by this member."
                )

            borrowed.remove(book_id)
            member[3] = ",".join(borrowed)

            break

    if not member_found:
        raise MemberNotFoundError(
            "Error: Member not found."
        )

    # Update Book Status
    for book in books:

        if book[0] == book_id:

            book_found = True
            book[4] = "Available"
            break

    if not book_found:
        raise BookNotFoundError(
            "Error: Book not found."
        )

    write_books(books)
    write_members(members)

    print("Book returned successfully.")