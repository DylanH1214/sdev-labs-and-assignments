from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(120), nullable=False)
    publisher = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"{self.book_name} by {self.author} (Publisher: {self.publisher})"

# Home route
@app.route('/')
def index():
    return 'Welcome to the Book API!'

# Get all books
@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {
            'id': book.id,
            'book_name': book.book_name,
            'author': book.author,
            'publisher': book.publisher
        }
        output.append(book_data)

    return {"books": output}

# Get a single book by ID
@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {
        "id": book.id,
        "book_name": book.book_name,
        "author": book.author,
        "publisher": book.publisher
    }

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    book = Book(
        book_name=request.json['book_name'],
        author=request.json['author'],
        publisher=request.json['publisher']
    )
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

# Delete a book by ID
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "Book not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": f"Book {id} deleted successfully"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)