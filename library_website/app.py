from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db_connection import get_db_connection
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key
app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Role-Based Access Control Decorator
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                return "Access denied. You do not have permission to view this page."
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home Route with PDF Upload
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        semester = request.form.get('semester')
        subject = request.form.get('subject')
        file = request.files.get('file')
        
        if file and allowed_file(file.filename):
            filename = f"{semester}_{subject}.pdf"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Insert the book into the Book table
            connection = get_db_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    sql = "INSERT INTO Book (Title, Semester) VALUES (%s, %s)"
                    val = (subject, semester)
                    cursor.execute(sql, val)
                    connection.commit()
                    print(f"Added book: {subject} for Semester {semester}")  # Debugging
                    return 'File uploaded and book added successfully!'
                except Exception as e:
                    print(f"Error inserting book: {e}")
                    connection.rollback()
                    return 'File uploaded, but failed to add book to database.'
                finally:
                    cursor.close()
                    connection.close()
            else:
                return 'Database connection failed.'
        else:
            return 'Invalid file type. Only PDFs are allowed.'
    
    return render_template('index.html')

# Book List (All Books)
@app.route('/books')
def book_list():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            sql = """
                SELECT b.BookID AS ID, b.Title AS Title, b.ISBN, b.PublicationYear, b.Genre, b.Publisher, b.Edition, a.AuthorName AS Author
                FROM Book b
                LEFT JOIN Author a ON b.AuthorID = a.AuthorID
            """
            cursor.execute(sql)
            books = cursor.fetchall()
            print(f"Fetched all books: {books}")  # Detailed debugging
            return render_template('index.html', books=books)
        except Exception as e:
            print(f"Error fetching books: {e}")
            return "Failed to fetch books."
        finally:
            cursor.close()
            connection.close()
    else:
        return "Database connection failed."

# Detailed Books by Semester
@app.route('/semester_books/<int:semester>')
def semester_books(semester):
    print(f"Requested semester: {semester}")  # Debugging
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
            print(f"Fetched books for semester {semester}: {books}")  # Detailed debugging
            if not books:
                print("No books found for this semester")
            return render_template('index.html', books=books, semester=semester)
        except Exception as e:
            print(f"Error fetching books by semester: {e}")
            return "Failed to fetch books."
        finally:
            cursor.close()
            connection.close()
    else:
        return "Database connection failed."

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        hashed_password = generate_password_hash(password)

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                sql = """
                    INSERT INTO Users (Name, Email, Password, Role)
                    VALUES (%s, %s, %s, %s)
                """
                val = (name, email, hashed_password, role)
                cursor.execute(sql, val)
                connection.commit()
                return "User registered successfully!"
            except Exception as e:
                print(f"Error registering user: {e}")
                connection.rollback()
                return "Failed to register user."
            finally:
                cursor.close()
                connection.close()
        else:
            return "Database connection failed."
    
    return '''
    <form method="post">
        Name: <input type="text" name="name" required><br>
        Email: <input type="email" name="email" required><br>
        Password: <input type="password" name="password" required><br>
        Role: 
        <select name="role">
            <option value="student">Student</option>
            <option value="faculty">Faculty</option>
            <option value="staff">Staff</option>
        </select><br>
        <button type="submit">Register</button>
    </form>
    '''

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = "SELECT * FROM Users WHERE Email = %s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()

                if user and check_password_hash(user['Password'], password):
                    session['user_id'] = user['UserID']
                    session['role'] = user['Role']
                    return f"Logged in as {user['Role']}. Welcome, {user['Name']}!"
                else:
                    return "Invalid email or password."
            except Exception as e:
                print(f"Error during login: {e}")
                return "Login failed."
            finally:
                cursor.close()
                connection.close()
        else:
            return "Database connection failed."
    
    return '''
    <form method="post">
        Email: <input type="email" name="email" required><br>
        Password: <input type="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    '''

# User Logout
@app.route('/logout')
def logout():
    session.clear()
    return "You have been logged out."

# Advanced Search
@app.route('/advanced_search', methods=['GET', 'POST'])
def advanced_search():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        subject = request.form.get('subject')
        isbn = request.form.get('isbn')
        course_code = request.form.get('course_code')

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                sql = """
                    SELECT b.BookID AS ID, b.Title AS Title, b.ISBN, b.PublicationYear, b.Genre, b.Publisher, b.Edition, a.AuthorName AS Author
                    FROM Book b
                    LEFT JOIN Author a ON b.AuthorID = a.AuthorID
                    WHERE (%s IS NULL OR b.Title LIKE %s)
                      AND (%s IS NULL OR a.AuthorName LIKE %s)
                      AND (%s IS NULL OR b.Genre LIKE %s)
                      AND (%s IS NULL OR b.ISBN = %s)
                      AND (%s IS NULL OR b.Genre LIKE %s)
                """
                val = (
                    title, f"%{title}%" if title else None,
                    author, f"%{author}%" if author else None,
                    subject, f"%{subject}%" if subject else None,
                    isbn, isbn,
                    course_code, f"%{course_code}%" if course_code else None
                )
                cursor.execute(sql, val)
                books = cursor.fetchall()
                print(f"Fetched books from search: {books}")  # Detailed debugging
                return render_template('index.html', books=books)
            except Exception as e:
                print(f"Error during advanced search: {e}")
                return "Search failed."
            finally:
                cursor.close()
                connection.close()
        else:
            return "Database connection failed."
    
    return render_template('index.html')

# Issue Book
@app.route('/issue_book', methods=['POST'])
@role_required('staff')
def issue_book():
    book_id = request.form['book_id']
    member_id = request.form['member_id']

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = """
                INSERT INTO Borrowing (BookID, MemberID, BorrowDate, DueDate)
                VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 14 DAY))
            """
            val = (book_id, member_id)
            cursor.execute(sql, val)
            connection.commit()
            return "Book issued successfully!"
        except Exception as e:
            print(f"Error issuing book: {e}")
            connection.rollback()
            return "Failed to issue book."
        finally:
            cursor.close()
            connection.close()
    else:
        return "Database connection failed."

# Return Book
@app.route('/return_book/<int:borrow_id>', methods=['POST'])
@role_required('staff')
def return_book(borrow_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "UPDATE Borrowing SET ReturnDate = CURDATE() WHERE BorrowID = %s"
            cursor.execute(sql, (borrow_id,))
            connection.commit()
            return "Book returned successfully!"
        except Exception as e:
            print(f"Error returning book: {e}")
            connection.rollback()
            return "Failed to return book."
        finally:
            cursor.close()
            connection.close()
    else:
        return "Database connection failed."

# Reserve Book
@app.route('/reserve_book/<int:book_id>', methods=['POST'])
def reserve_book(book_id):
    member_id = session.get('user_id')
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Reservations (BookID, MemberID, ReservationDate) VALUES (%s, %s, CURDATE())"
            val = (book_id, member_id)
            cursor.execute(sql, val)
            connection.commit()
            return "Book reserved successfully!"
        except Exception as e:
            print(f"Error reserving book: {e}")
            connection.rollback()
            return "Failed to reserve book."
        finally:
            cursor.close()
            connection.close()
    else:
        return "Database connection failed."

# Renew Book
@app.route('/renew_book/<int:borrow_id>', methods=['POST'])
def renew_book(borrow_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            sql = "UPDATE Borrowing SET DueDate = DATE_ADD(DueDate, INTERVAL 7 DAY) WHERE BorrowID = %s"
            cursor.execute(sql, (borrow_id,))
            connection.commit()
            return "Book renewed successfully!"
        except Exception as e:
            print(f"Error renewing book: {e}")
            connection.rollback()
            return "Failed to renew book."
        finally:
            cursor.close()
            connection.close()
    else:
        return "Database connection failed."

if __name__ == '__main__':
    app.run(debug=True)