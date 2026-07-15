from services.library_service import (
    view_books,
    add_book,
    register_member,
    borrow_book,
    return_book
)

from exceptions.custom_exceptions import (
    BookNotFoundError,
    MemberNotFoundError,
    BookAlreadyBorrowedError,
    BookNotBorrowedError
)


def menu():
    while True:

        print("\n========== Library Management System ==========")
        print("1. View Books")
        print("2. Add Book")
        print("3. Register Member")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")

        choice = input("Enter your choice: ")

        try:

            if choice == "1":
                view_books()

            elif choice == "2":

                book_id = input("Enter Book ID: ")
                title = input("Enter Title: ")
                author = input("Enter Author: ")
                category = input("Enter Category: ")

                add_book(book_id, title, author, category)

            elif choice == "3":

                member_id = input("Enter Member ID: ")
                name = input("Enter Member Name: ")
                email = input("Enter Email: ")

                register_member(member_id, name, email)

            elif choice == "4":

                member_id = input("Enter Member ID: ")
                book_id = input("Enter Book ID: ")

                borrow_book(member_id, book_id)

            elif choice == "5":

                member_id = input("Enter Member ID: ")
                book_id = input("Enter Book ID: ")

                return_book(member_id, book_id)

            elif choice == "6":

                print("\nThank you for using the Library Management System.")
                break

            else:
                print("Invalid choice. Please try again.")

        except BookNotFoundError as e:
            print(e)

        except MemberNotFoundError as e:
            print(e)

        except BookAlreadyBorrowedError as e:
            print(e)

        except BookNotBorrowedError as e:
            print(e)

        except FileNotFoundError:
            print("Error: Data file not found.")

        except Exception as e:
            print("Unexpected Error:", e)


if __name__ == "__main__":
    menu()