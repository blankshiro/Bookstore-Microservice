import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    os.environ.get("db_conn_wishlist") + "/wishlist"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size": 100,
    "pool_recycle": 280
}

db = SQLAlchemy(app)
CORS(app)


class WishlistItem(db.Model):
    __tablename__ = "item"
    __table_args__ = (
        db.UniqueConstraint("user_id", "book_id"),
    )

    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, book_id):
        self.set_cols(user_id, book_id)

    def set_cols(self, user_id, book_id):
        self.user_id = user_id
        self.book_id = book_id

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "user_id": self.user_id,
            "book_id": self.book_id
        }


@app.route("/health")
def health_check():
    return jsonify(
        {
            "message": "Service is healthy."
        }
    ), 200


@app.route("/wishlist")
def get_all_by_query():
    args = request.args
    try:
        if len(args.keys()) > 2:
            raise ValueError("Too many query parameters.")
        if not set(args.keys()) <= {"user", "book"}:
            raise ValueError("Unknown query parameter(s).")
        if set(args.keys()) == {"user", "book"}:
            raise ValueError("Query keys 'user' and 'book' cannot "
                             "both be provided at the same time.")

        filter_params = {}
        if "user" in args.keys():
            filter_params["user_id"] = int(args["user"])
        if "book" in args.keys():
            filter_params["book_id"] = int(args["book"])
        item_list = WishlistItem.query.filter_by(**filter_params).all()
    except Exception as e:
        return jsonify(
            {
                "message": "Invalid query string.",
                "error": str(e)
            }
        ), 500
    if len(item_list) == 0:
        return jsonify(
            {
                "message": "There are no items."
            }
        ), 404
    return jsonify(
        {
            "data": {
                "items": [item.to_dict() for item in item_list]
            }
        }
    ), 200


@app.route("/wishlist/<int:item_id>")
def find_by_id(item_id):
    item = WishlistItem.query.filter_by(item_id=item_id).first()
    if item is None:
        return jsonify(
            {
                "message": "Item not found."
            }
        ), 404
    return jsonify(
        {
            "data": item.to_dict()
        }
    ), 200


@app.route("/wishlist", methods=["POST"])
def new_item():
    try:
        data = request.get_json()
        item = WishlistItem(**data)
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred creating the item.",
                "error": str(e)
            }
        ), 500
    return jsonify(
        {
            "data": item.to_dict()
        }
    ), 201


@app.route("/wishlist/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = WishlistItem.query.filter_by(item_id=item_id).first()
    if item is None:
        return jsonify(
            {
                "message": "Item not found."
            }
        ), 404
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred deleting the item.",
                "error": str(e)
            }
        ), 500
    return jsonify(
        {
            "data": {
                "item_id": item_id
            }
        }
    ), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
