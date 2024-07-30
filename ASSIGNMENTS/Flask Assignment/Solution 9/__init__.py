from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    api = Api(app)

    from .resources.book import BookListResource, BookResource
    api.add_resource(BookListResource, '/books')
    api.add_resource(BookResource, '/books/<int:book_id>')

    with app.app_context():
        db.create_all()

    return app
