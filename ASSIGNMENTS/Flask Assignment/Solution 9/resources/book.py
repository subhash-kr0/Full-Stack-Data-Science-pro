from flask_restful import Resource, reqparse
from app import db
from models import Book

book_parser = reqparse.RequestParser()
book_parser.add_argument('title', type=str, required=True, help="Title of the book is required")
book_parser.add_argument('author', type=str, required=True, help="Author of the book is required")
book_parser.add_argument('year_published', type=int, required=True, help="Year published of the book is required")

class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'year_published': book.year_published
        }

    def put(self, book_id):
        book = Book.query.get_or_404(book_id)
        args = book_parser.parse_args()
        book.title = args['title']
        book.author = args['author']
        book.year_published = args['year_published']
        db.session.commit()
        return {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'year_published': book.year_published
        }

    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return '', 204

class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return [
            {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'year_published': book.year_published
            } for book in books
        ]

    def post(self):
        args = book_parser.parse_args()
        book = Book(
            title=args['title'],
            author=args['author'],
            year_published=args['year_published']
        )
        db.session.add(book)
        db.session.commit()
        return {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'year_published': book.year_published
        }, 201
