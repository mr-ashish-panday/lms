# database_operations.py
import mysql.connector
from db_connection import get_db_connection

def get_all_books():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT BookID, ISBN, Title, PublicationYear, Genre, Publisher, Edition, AuthorID FROM Book")
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
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "SELECT BookID, ISBN, Title, PublicationYear, Genre, Publisher, Edition, AuthorID FROM Book WHERE BookID = %s"
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
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Member (Name, Address, ContactNumber, Email) VALUES (%s, %s, %s, %s)"
            val = (name, address, contact_number, email)
            cursor.execute(sql, val)
            connection.commit()
            return cursor.lastrowid  # Returns the ID of the newly inserted member
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
            return cursor.rowcount  # Returns the number of rows affected (1 if successful, 0 if not found)
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
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "DELETE FROM Book WHERE BookID = %s"
            cursor.execute(sql, (book_id,))
            connection.commit()
            return cursor.rowcount  # Returns the number of rows affected (1 if successful, 0 if not found)
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
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Added BookID to the query
            sql = """
                SELECT BookID, ISBN, Title, PublicationYear, Genre, Publisher, Edition, AuthorID
                FROM Book
                WHERE Title LIKE %s OR AuthorID IN (SELECT AuthorID FROM Author WHERE AuthorName LIKE %s)
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
#Add borrow book and other function
def borrow_book(book_id, member_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Borrowing (BookID, MemberID, BorrowDate, DueDate) VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY))"
            val = (book_id, member_id)
            cursor.execute(sql, val)
            connection.commit()
            return cursor.lastrowid
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

def get_overdue_books():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
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