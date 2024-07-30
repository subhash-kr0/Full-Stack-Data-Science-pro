from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

from resources.book import BookListResource, BookResource
api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True)
