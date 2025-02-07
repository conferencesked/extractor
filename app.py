from flask import Flask, jsonify, request

app = Flask(__name__)

books = []

# Helper function to generate IDs
def generate_id():
    return len(books) + 1

# Endpoint to get all books
@app.route('/reading-list/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

# Endpoint to add a new book
@app.route('/reading-list/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book = {
        'id': generate_id(),
        'author': data['author'],
        'name': data['name'],
        'status': data['status']
    }
    books.append(book)
    return jsonify(book)

# Endpoint to process a URL within the books service
@app.route('/reading-list/books/process-url/<path:url>', methods=['GET'])
def process_url(url):
    """
    Accepts a URL as a route parameter and processes it by
    removing 'www.' and '.com'.
    """
    # Remove 'www.' and '.com' from the URL
    processed_url = url.replace('www.', '').replace('.com', '')
    return jsonify({'processed_url': processed_url})

# Endpoint to get a book by ID
@app.route('/reading-list/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Retrieves a book by its ID.
    """
    for book in books:
        if book['id'] == book_id:
            return jsonify(book)
    return '', 404
    
if __name__ == '__main__':
    app.run()
