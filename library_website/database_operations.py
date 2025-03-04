import mysql.connector
from db_connection import get_db_connection

def get_all_books():
    """
    Retrieve all books from the Book table with their details and author information.
    
    Returns:
        list: List of tuples containing book details (BookID, ISBN, Title, PublicationYear, Genre, Publisher, Edition, AuthorID).
        None: If there's an error or database connection fails.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  # Use dictionary for consistency with app.py
            sql = """
                SELECT b.BookID, b.ISBN, b.Title, b.PublicationYear, b.Genre, b.Publisher, b.Edition, a.AuthorID, a.AuthorName
                FROM Book b
                LEFT JOIN Author a ON b.AuthorID = a.AuthorID
            """
            cursor.execute(sql)
            books = cursor.fetchall()
            return books
        except mysql.connector.Error as e:
            print(f"Error retrieving all books: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def get_book_by_id(book_id):
    """
    Retrieve a specific book by its ID, including author information.
    
    Args:
        book_id (int): The ID of the book to retrieve.
    
    Returns:
        dict: Dictionary containing book details, or None if not found or error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            sql = """
                SELECT b.BookID, b.ISBN, b.Title, b.PublicationYear, b.Genre, b.Publisher, b.Edition, b.AuthorID, a.AuthorName
                FROM Book b
                LEFT JOIN Author a ON b.AuthorID = a.AuthorID
                WHERE b.BookID = %s
            """
            cursor.execute(sql, (book_id,))
            book = cursor.fetchone()
            return book
        except mysql.connector.Error as e:
            print(f"Error retrieving book by ID: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def add_new_member(name, address, contact_number, email):
    """
    Add a new member to the Member table.
    
    Args:
        name (str): Member's name.
        address (str): Member's address.
        contact_number (str): Member's contact number.
        email (str): Member's email.
    
    Returns:
        int: The ID of the newly inserted member, or None if error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Member (Name, Address, ContactNumber, Email) VALUES (%s, %s, %s, %s)"
            val = (name, address, contact_number, email)
            cursor.execute(sql, val)
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"Error adding new member: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def update_book(book_id, isbn, title, publication_year, genre, publisher, edition, number_of_copies):
    """
    Update an existing book's details in the Book table.
    
    Args:
        book_id (int): The ID of the book to update.
        isbn (str): Book's ISBN.
        title (str): Book's title.
        publication_year (int): Book's publication year.
        genre (str): Book's genre.
        publisher (str): Book's publisher.
        edition (str): Book's edition.
        number_of_copies (int): Number of copies available.
    
    Returns:
        int: Number of rows affected (1 if successful, 0 if not found), or None if error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
                UPDATE Book
                SET ISBN = %s, Title = %s, PublicationYear = %s, Genre = %s,
                    Publisher = %s, Edition = %s, NumberOfCopies = %s
                WHERE BookID = %s
            """
            val = (isbn, title, publication_year, genre, publisher, edition, number_of_copies, book_id)
            cursor.execute(sql, val)
            connection.commit()
            return cursor.rowcount
        except mysql.connector.Error as e:
            print(f"Error updating book: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def delete_book(book_id):
    """
    Delete a book from the Book table by its ID.
    
    Args:
        book_id (int): The ID of the book to delete.
    
    Returns:
        int: Number of rows affected (1 if successful, 0 if not found), or None if error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM Book WHERE BookID = %s"
            cursor.execute(sql, (book_id,))
            connection.commit()
            return cursor.rowcount
        except mysql.connector.Error as e:
            print(f"Error deleting book: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def search_books(search_term):
    """
    Search for books by title or author name.
    
    Args:
        search_term (str): The term to search for in titles or author names.
    
    Returns:
        list: List of dictionaries containing book details, or None if error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            sql = """
                SELECT b.BookID, b.ISBN, b.Title, b.PublicationYear, b.Genre, b.Publisher, b.Edition, b.AuthorID, a.AuthorName
                FROM Book b
                LEFT JOIN Author a ON b.AuthorID = a.AuthorID
                WHERE b.Title LIKE %s OR a.AuthorName LIKE %s
            """
            val = ('%' + search_term + '%', '%' + search_term + '%')
            cursor.execute(sql, val)
            books = cursor.fetchall()
            return books
        except mysql.connector.Error as e:
            print(f"Error searching books: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def borrow_book(book_id, member_id):
    """
    Borrow a book for a member, setting a 14-day due date.
    
    Args:
        book_id (int): The ID of the book to borrow.
        member_id (int): The ID of the member borrowing the book.
    
    Returns:
        int: The ID of the new borrowing record, or None if error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Check if book is available (NumberOfCopies > 0 and not already borrowed)
            cursor.execute("SELECT NumberOfCopies FROM Book WHERE BookID = %s", (book_id,))
            book = cursor.fetchone()
            if book and book[0] > 0:
                cursor.execute("""
                    SELECT COUNT(*) FROM Borrowing 
                    WHERE BookID = %s AND ReturnDate IS NULL
                """, (book_id,))
                borrowed_count = cursor.fetchone()[0]
                if borrowed_count < book[0]:  # Ensure copies are available
                    sql = """
                        INSERT INTO Borrowing (BookID, MemberID, BorrowDate, DueDate)
                        VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY))
                    """
                    val = (book_id, member_id)
                    cursor.execute(sql, val)
                    connection.commit()
                    return cursor.lastrowid
                else:
                    print("No available copies of this book.")
                    return None
            else:
                print("Book not found or no copies available.")
                return None
        except mysql.connector.Error as e:
            print(f"Error borrowing book: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def return_book(borrowing_id):
    """
    Return a borrowed book, updating the return date.
    
    Args:
        borrowing_id (int): The ID of the borrowing record.
    
    Returns:
        int: Number of rows affected (1 if successful, 0 if not found), or None if error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "UPDATE Borrowing SET ReturnDate = CURDATE() WHERE BorrowingID = %s"
            cursor.execute(sql, (borrowing_id,))
            connection.commit()
            return cursor.rowcount
        except mysql.connector.Error as e:
            print(f"Error returning book: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def reserve_book(book_id, member_id):
    """
    Reserve a book for a member.
    
    Args:
        book_id (int): The ID of the book to reserve.
        member_id (int): The ID of the member reserving the book.
    
    Returns:
        int: The ID of the new reservation record, or None if error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Reservations (BookID, MemberID, ReservationDate) VALUES (%s, %s, CURDATE())"
            val = (book_id, member_id)
            cursor.execute(sql, val)
            connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as e:
            print(f"Error reserving book: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def renew_book(borrowing_id):
    """
    Renew a borrowed book, extending the due date by 7 days.
    
    Args:
        borrowing_id (int): The ID of the borrowing record.
    
    Returns:
        int: Number of rows affected (1 if successful, 0 if not found), or None if error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "UPDATE Borrowing SET DueDate = DATE_ADD(DueDate, INTERVAL 7 DAY) WHERE BorrowingID = %s"
            cursor.execute(sql, (borrowing_id,))
            connection.commit()
            return cursor.rowcount
        except mysql.connector.Error as e:
            print(f"Error renewing book: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def get_overdue_books():
    """
    Retrieve all overdue books (where DueDate has passed and ReturnDate is NULL).
    
    Returns:
        list: List of dictionaries containing borrowing details (BorrowingID, BookID, MemberID, BorrowDate, DueDate, ReturnDate, MemberName, BookTitle).
        None: If there's an error or database connection fails.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            sql = """
                SELECT b.BorrowingID, b.BookID, b.MemberID, b.BorrowDate, b.DueDate, b.ReturnDate,
                       m.Name AS MemberName,
                       bk.Title AS BookTitle
                FROM Borrowing b
                INNER JOIN Member m ON b.MemberID = m.MemberID
                INNER JOIN Book bk ON b.BookID = bk.BookID
                WHERE b.DueDate < CURDATE() AND b.ReturnDate IS NULL
            """
            cursor.execute(sql)
            overdue_books = cursor.fetchall()
            return overdue_books
        except mysql.connector.Error as e:
            print(f"Error retrieving overdue books: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None

def get_books_by_semester(semester):
    """
    Retrieve all books for a specific semester, including author information.
    
    Args:
        semester (int): The semester number to filter books by.
    
    Returns:
        list: List of dictionaries containing book details, or None if error occurs.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            sql = """
                SELECT b.BookID AS ID, b.Title AS Title, b.ISBN, b.PublicationYear, b.Genre, b.Publisher, b.Edition, a.AuthorName AS Author
                FROM Book b
                LEFT JOIN Author a ON b.AuthorID = a.AuthorID
                WHERE b.Semester = %s
            """
            cursor.execute(sql, (semester,))
            books = cursor.fetchall()
            return books
        except mysql.connector.Error as e:
            print(f"Error retrieving books by semester: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    else:
        return None