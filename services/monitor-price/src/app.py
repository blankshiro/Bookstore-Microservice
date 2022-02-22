import os
import json

import requests
import pika

import amqp_setup

users_service_url = os.environ.get("users_service_url_internal")
wishlist_service_url = os.environ.get("wishlist_service_url_internal")

if os.environ.get("stage") == "production":
    users_service_url = os.environ.get("users_service_url")
    wishlist_service_url = os.environ.get("wishlist_service_url")

json_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def callback(channel, method, properties, body):
    message_body = json.loads(body)
    book_id = message_body["book_id"]
    wishlist_resp = requests.get(
        f"{wishlist_service_url}/wishlist?book={book_id}",
        headers=json_headers)
    if wishlist_resp.status_code != 200:
        return
    for wishlist_item in wishlist_resp.json()["data"]["items"]:
        # No need to double check user existence
        user_id = wishlist_item["user_id"]
        email = requests.get(
            f"{users_service_url}/users/{user_id}",
            headers=json_headers).json()["email"]
        notification_data = {
            "email": email,
            "data": message_body
        }
        cnx = pika.BlockingConnection(amqp_setup.params)
        channel = cnx.channel()

        channel.basic_publish(
            exchange=amqp_setup.exch_name, routing_key="wishlist.info",
            body=json.dumps(notification_data),
            properties=pika.BasicProperties(delivery_mode=2))

        cnx.close()


amqp_setup.channel.basic_consume(
    queue=amqp_setup.queue_name_2,
    on_message_callback=callback, auto_ack=True)
amqp_setup.channel.start_consuming()
