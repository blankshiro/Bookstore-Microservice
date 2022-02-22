import os
import json

import requests
import pika

from flask import Flask, request, jsonify
from flask_cors import CORS

import amqp_setup

books_service_url = os.environ.get("books_service_url_internal")
users_service_url = os.environ.get("users_service_url_internal")
wishlist_service_url = os.environ.get("wishlist_service_url_internal")

if os.environ.get("stage") == "production":
    books_service_url = os.environ.get("books_service_url")
    users_service_url = os.environ.get("users_service_url")
    wishlist_service_url = os.environ.get("wishlist_service_url")

json_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

app = Flask(__name__)

CORS(app)


@app.route("/health")
def health_check():
    return jsonify(
        {
            "message": "Service is healthy."
        }
    ), 200


@app.route("/save-wishlist", methods=["POST"])
def save_wishlist():
    def undo_creations(item_list):
        for item_data in item_list:
            requests.delete(
                f"{wishlist_service_url}/wishlist/{item_data['item_id']}",
                headers=json_headers)

    data = request.get_json()
    # First, find the user
    user_resp = requests.get(
        f"{users_service_url}/users/{data['user_id']}",
        headers=json_headers)
    if user_resp.status_code != 200:
        return jsonify(
            {
                "message": "Unable to save wishlist.",
                "error": "Unable to find user record."
            }
        ), 500
    email = user_resp.json()["email"]

    # Next, create the wishlist items
    item_list = []
    wishlist_books = data["wishlist_books"]
    for book_data in wishlist_books:
        book_resp = requests.get(
            f"{books_service_url}/products/{book_data['book_id']}",
            headers=json_headers)
        if book_resp.status_code != 200:
            undo_creations(item_list)
            return jsonify(
                {
                    "message": "Unable to save wishlist.",
                    "error": "Unable to find book record."
                }
            ), 500

        create_resp = requests.post(
            f"{wishlist_service_url}/wishlist",
            data=json.dumps(
                {
                    "user_id": data["user_id"],
                    "book_id": book_data["book_id"]
                }
            ), headers=json_headers)
        if create_resp.status_code != 201:
            undo_creations(item_list)
            return jsonify(
                {
                    "message": "Unable to save wishlist.",
                    "error": "Unable to create item record."
                }
            ), 500
        item_list.append(create_resp.json()["data"])

    # Finally, send the notification
    notification_data = {
        "email": email,
        "data": wishlist_books
    }
    cnx = pika.BlockingConnection(amqp_setup.params)
    channel = cnx.channel()

    channel.basic_publish(
        exchange=amqp_setup.exch_name, routing_key="wishlist.new",
        body=json.dumps(notification_data),
        properties=pika.BasicProperties(delivery_mode=2))

    cnx.close()
    return jsonify(
        {
            "message": "Wishlist saved.",
            "data": item_list
        }
    ), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
