import csv
import os

BOOKS_FILE = "data/books.csv"
MEMBERS_FILE = "data/members.csv"


# -------------------- BOOK FILE --------------------

def read_books():
    books = []

    if not os.path.exists(BOOKS_FILE):
        raise FileNotFoundError("Books file not found.")

    with open(BOOKS_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        for row in reader:
            books.append(row)

    return books


def write_books(books):
    with open(BOOKS_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["BookID", "Title", "Author", "Category", "Status"])

        writer.writerows(books)


# -------------------- MEMBER FILE --------------------

def read_members():
    members = []

    if not os.path.exists(MEMBERS_FILE):
        raise FileNotFoundError("Members file not found.")

    with open(MEMBERS_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            members.append(row)

    return members


def write_members(members):
    with open(MEMBERS_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(
            ["MemberID", "Name", "Email", "BorrowedBooks"]
        )

        writer.writerows(members)