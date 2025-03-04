# main.py
from library_website.database_operations import get_all_books, get_book_by_id, add_new_member, \
    update_book, delete_book, search_books, borrow_book, return_book, get_overdue_books

def list_all_books():
    books = get_all_books()
    if books:
        print("\n--- All Books ---")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[2]}, AuthorID: {book[7]}")  # index access
    else:
        print("Could not retrieve books.")

def search_book_by_id():
    try:
        book_id = int(input("Enter book ID to search: "))
        book = get_book_by_id(book_id)
        if book:
            print(f"Book ID: {book[0]}, ISBN: {book[1]}, Title: {book[2]}, PublicationYear: {book[3]}, Genre: {book[4]}, Author: {book[7]}")  # index access
        else:
            print("Book not found.")
    except ValueError:
        print("Invalid book ID. Please enter a number.")

def register_new_member():
    name = input("Enter member name: ")
    address = input("Enter member address: ")
    contact_number = input("Enter member contact number: ")
    email = input("Enter member email: ")

    member_id = add_new_member(name, address, contact_number, email)
    if member_id:
        print(f"New member registered with ID: {member_id}")
    else:
        print("Failed to register new member.")

def update_book_info():
    try:
        book_id = int(input("Enter book ID to update: "))
        isbn = input("Enter new ISBN: ")
        title = input("Enter new title: ")
        publication_year = int(input("Enter new publication year: "))
        genre = input("Enter new genre: ")
        publisher = input("Enter new publisher: ")
        edition = input("Enter new edition: ")
        number_of_copies = int(input("Enter new number of copies: "))

        rows_affected = update_book(book_id, isbn, title, publication_year, genre, publisher, edition, number_of_copies)
        if rows_affected:
            print(f"Book with ID {book_id} updated successfully.")
        else:
            print(f"Book with ID {book_id} not found or update failed.")
    except ValueError:
        print("Invalid input. Please enter valid values.")

def delete_book_record():
    try:
        book_id = int(input("Enter book ID to delete: "))
        rows_affected = delete_book(book_id)
        if rows_affected:
            print(f"Book with ID {book_id} deleted successfully.")
        else:
            print(f"Book with ID {book_id} not found or deletion failed.")
    except ValueError:
        print("Invalid book ID. Please enter a number.")

def search_books_by_term():
    search_term = input("Enter search term (title or author): ")
    books = search_books(search_term)
    if books:
        print("\n--- Search Results ---")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[2]}, Author: {book[7]}")  # index access
    else:
        print("No books found matching the search term.")

def borrow_a_book():
    try:
        book_id = int(input("Enter Book ID to borrow: "))
        member_id = int(input("Enter Member ID: "))

        borrowing_id = borrow_book(book_id, member_id)
        if borrowing_id:
            print(f"Book with ID {book_id} borrowed successfully by member {member_id}. Borrowing ID is {borrowing_id}")
        else:
            print("Book Borrowing Failed.")
    except ValueError:
        print("Invalid ID. Please enter a number.")

def return_a_book():
    try:
        borrowing_id = int(input("Enter Borrowing ID to return: "))
        rows_affected = return_book(borrowing_id)
        if rows_affected:
            print(f"Book with Borrowing ID {borrowing_id} returned successfully.")
        else:
            print(f"Book Borrowing with ID {borrowing_id} not found or return failed.")
    except ValueError:
        print("Invalid Book Borrowing ID. Please enter a number.")

def view_overdue_books():
    overdue_books = get_overdue_books()
    if overdue_books:
        print("\n--- Overdue Books ---")
        for book in overdue_books:
            print(f"BorrowingID: {book[0]}, Book: {book[7]}, Member: {book[6]}, Due Date: {book[4]}")  # index access
    else:
        print("No overdue books found.")

def main_menu():
    while True:
        print("\n--- Library Management System ---")
        print("1. List all books")
        print("2. Search book by ID")
        print("3. Register new member")
        print("4. Update book information")
        print("5. Delete book")
        print("6. Search books by title or author")
        print("7. Borrow a book")
        print("8. Return a book")
        print("9. View overdue books")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            list_all_books()
        elif choice == '2':
            search_book_by_id()
        elif choice == '3':
            register_new_member()
        elif choice == '4':
            update_book_info()
        elif choice == '5':
            delete_book_record()
        elif choice == '6':
            search_books_by_term()
        elif choice == '7':
            borrow_a_book()
        elif choice == '8':
            return_a_book()
        elif choice == '9':
            view_overdue_books()
        elif choice == '10':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()