import os
import json

import pika

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

disable_amqp = int(os.environ.get("disable_amqp", "0"))
if not disable_amqp:
    import amqp_setup

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    os.environ.get("db_conn_books") + "/product"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size": 100,
    "pool_recycle": 280
}

db = SQLAlchemy(app)
CORS(app)


class Book(db.Model):
    __tablename__ = "product"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    isbn = db.Column(db.String(16), nullable=False)
    author = db.Column(db.String(32), nullable=False)
    publisher = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self, title, isbn, author, publisher, price, stock):
        self.set_cols(title, isbn, author, publisher, price, stock)

    def set_cols(self, title, isbn, author, publisher, price, stock):
        self.title = title
        self.isbn = isbn
        self.author = author
        self.publisher = publisher
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "isbn": self.isbn,
            "author": self.author,
            "publisher": self.publisher,
            "price": self.price,
            "stock": self.stock
        }


@app.route("/health")
def health_check():
    return jsonify(
        {
            "message": "Service is healthy."
        }
    ), 200


@app.route("/products")
def get_all():
    book_list = Book.query.all()
    if len(book_list) == 0:
        return jsonify(
            {
                "message": "There are no books."
            }
        ), 404
    return jsonify(
        {
            "data": {
                "books": [book.to_dict() for book in book_list]
            }
        }
    ), 200


@app.route("/products/<int:book_id>")
def find_by_id(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        return jsonify(
            {
                "message": "Book not found."
            }
        ), 404
    return jsonify(
        {
            "data": book.to_dict()
        }
    ), 200


@app.route("/products", methods=["POST"])
def new_book():
    try:
        data = request.get_json()
        book = Book(**data)
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred creating the book.",
                "error": str(e)
            }
        ), 500
    return jsonify(
        {
            "data": book.to_dict()
        }
    ), 201


@app.route("/products/<int:book_id>", methods=["PUT"])
def replace_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        return jsonify(
            {
                "message": "Book not found."
            }
        ), 404
    try:
        data = request.get_json()
        book.set_cols(**data)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred replacing the book.",
                "error": str(e)
            }
        ), 500
    return jsonify(
        {
            "data": book.to_dict()
        }
    ), 200


@app.route("/products/<int:book_id>", methods=["PATCH"])
def update_book(book_id):
    book = Book.query.with_for_update(of=Book)\
               .filter_by(book_id=book_id).first()
    if book is None:
        return jsonify(
            {
                "message": "Book not found."
            }
        ), 404
    try:
        old_price = book.price
        data = request.get_json()
        # Handle special case of reserving stock
        if "reserve" in data.keys():
            if len(data.keys()) > 1:
                raise ValueError("Key 'reserve' cannot be "
                                 "provided with other keys.")
            if data["reserve"] > book.stock:
                raise ValueError("Insufficient books in stock.")
            book.stock -= data["reserve"]
        else:
            new_data = {**book.to_dict(), **data}
            new_data.pop("book_id")
            book.set_cols(**new_data)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred updating the book.",
                "error": str(e)
            }
        ), 500
    # Handle price drop
    if not disable_amqp and book.price < old_price:
        cnx = pika.BlockingConnection(amqp_setup.params)
        channel = cnx.channel()

        channel.basic_publish(
            exchange=amqp_setup.exch_name, routing_key="book.price.drop",
            body=json.dumps(
                {
                    "book_id": book_id,
                    "old_price": old_price,
                    "new_price": book.price
                }
            ), properties=pika.BasicProperties(delivery_mode=2))

        cnx.close()
    return jsonify(
        {
            "data": book.to_dict()
        }
    ), 200


@app.route("/products/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if book is None:
        return jsonify(
            {
                "message": "Book not found."
            }
        ), 404
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred deleting the book.",
                "error": str(e)
            }
        ), 500
    return jsonify(
        {
            "data": {
                "book_id": book_id
            }
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
