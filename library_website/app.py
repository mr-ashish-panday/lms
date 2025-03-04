from flask import Flask, render_template, request, redirect, url_for
from database_operations import get_all_books, get_book_by_id, add_new_member, \
    update_book, delete_book, search_books, borrow_book, return_book, get_overdue_books

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render the index page

@app.route('/books')
def book_list():
    books = get_all_books()
    return render_template('book_list.html', books=books) # pass the books data to the template.

@app.route('/books/<int:book_id>')
def book_detail(book_id):
    book = get_book_by_id(book_id)
    if book:
        return render_template('book_detail.html', book=book)
    else:
        return "Book not found"

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        books = search_books(search_term)
        return render_template('book_list.html', books=books)
    else:
        return render_template('search.html')

@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        contact_number = request.form['contact_number']
        email = request.form['email']

        member_id = add_new_member(name, address, contact_number, email)
        if member_id:
            return f"New member registered with ID: {member_id}"
        else:
            return "Failed to register new member."
    else:
        return render_template('add_member.html')


if __name__ == '__main__':
    app.run(debug=True)  # Enable debug mode for development