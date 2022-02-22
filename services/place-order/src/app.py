import os
import requests
import datetime
import traceback
import pika
import json

from flask import Flask, request, jsonify
from flask_cors import CORS
import payment

app = Flask(__name__)

CORS(app)

product_service_url = os.environ.get("books_service_url_internal")
users_service_url = os.environ.get("users_service_url_internal")
wishlist_service_url = os.environ.get("wishlist_service_url_internal")
order_service_url = os.environ.get("orders_service_url_internal")

if os.environ.get("stage") == "production":
    product_service_url = os.environ.get("books_service_url")
    users_service_url = os.environ.get("users_service_url")
    wishlist_service_url = os.environ.get("wishlist_service_url")
    order_service_url = os.environ.get("orders_service_url")

print(f"order_service_url: {order_service_url}")


disable_amqp = int(os.environ.get("disable_amqp", "0"))
if not disable_amqp:
    import amqp_setup


@app.route("/placeorder/health")
def health_check():
    return jsonify(
        {
            "message": "Service is healthy."
        }
    ), 200


@app.route("/createorder", methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        user_id = data["user_id"]
        product_list = data["product_list"]
        card_details = data["card_details"]

        product_ids = []
        quantities = []
        for item in product_list:
            product_ids.append(item["product_id"])
            quantities.append(item["quantity"])
        for i in quantities:
            if i <= 0:
                return jsonify(
                    {
                        "message": "Invalid stock amount:" + str(i),
                    }
                ), 400

        order_list = []
        totalPrice = 0
        # print(type(product_service_url))
        # print(type(str(product_ids[0])))

        for i in range(len(product_ids)):
            product_url = product_service_url + "/products/" + \
                str(product_ids[i])
            status, price, book_title = reserve(product_url, product_ids[i],
                                                quantities[i])
            if status == 404:
                rollback(product_service_url, product_ids, quantities, i)
                return jsonify(
                    {
                        "message": "Invalid product. Product " +
                                   str(product_ids[i]) + " not found."
                    }
                ), 400
            elif status == 500:
                rollback(product_service_url, product_ids, quantities, i)
                return jsonify(
                    {
                        "message": "Invalid stock. Product " +
                                   str(product_ids[i]) +
                                   " has insufficient stock."
                    }
                ), 400
            totalPrice += price * quantities[i]
            order_list.append({
                "productId": product_ids[i],
                "quantity": quantities[i],
                "bookTitle": book_title,
                "price": price

            })
        print("check")
        try:
            res = payment.processPayment(totalPrice,
                                         "Chris Bookstore Order",
                                         card_details["cardNumber"],
                                         card_details["expiryMonth"],
                                         card_details["expiryYear"],
                                         card_details["cvv"])
            if not res:
                rollback(product_service_url, product_ids, quantities,
                         len(product_ids) - 1)
                return jsonify(
                    {
                        "message": "An error occurred creating the order.\
                         Transaction declined"
                    }
                ), 500
        except Exception as e:
            rollback(product_service_url, product_ids, quantities,
                     len(product_ids) - 1)
            return jsonify(
                {
                    "message": "An error occurred creating the order.1",
                    "error": str(e)
                }
            ), 400

        order_url = order_service_url + "/orders"
        order_request = requests.post(order_url, json={
            "userId": user_id,
            "datetime": str(datetime.datetime.now()),
            "totalPrice": totalPrice,
            "details": order_list
        })
        if order_request.status_code == 500:
            rollback(product_service_url, product_ids, quantities,
                     len(product_ids) - 1)
            return jsonify(
                {
                    "message": "An error occurred creating the order.2",
                }
            ), 500

        if not disable_amqp:
            message_body = json.dumps({
                "userId": user_id,
                "datetime": str(datetime.datetime.now()),
                "totalPrice": totalPrice,
                "details": order_list
            })
            json_headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

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
                exchange=amqp_setup.exch_name, routing_key="order.info",
                body=json.dumps(notification_data),
                properties=pika.BasicProperties(delivery_mode=2))

            cnx.close()

    except Exception as e:
        # print(traceback.format_exc())
        return jsonify(
            {
                "message": "An error occurred creating the order.3",
                "error": str(e),
                "traceback": str(traceback.format_exc())
            }
        ), 500

    return jsonify(
        {
            "message": "Order placed.",
        }
    ), 200


@app.route("/deleteorder", methods=['POST'])
def delete_order():
    try:
        data = request.get_json()
        order_id = data["order_id"]

        order_url = order_service_url + "/orders/" + str(order_id)
        order_request = requests.delete(order_url)
        # print(order_request.status_code)
        if order_request.status_code != 200:
            return jsonify(
                {
                    "message": "Order " + str(order_id) + " not found.",
                }
            ), 404

    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred deleting the order.",
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "message": "Order deleted.",
        }
    ), 200


def reserve(product_url, product_id, quantity):
    product_request = requests.patch(product_url, json={"reserve": quantity})

    if product_request.status_code != 200:
        return product_request.status_code, None, None
    return product_request.status_code,\
        product_request.json().get("data").get("price"),\
        product_request.json().get("data").get("title")


def rollback(product_service_url, product_ids, quantities, i):
    for j in range(i - 1, -1, -1):
        product_url = product_service_url + "/products/" + \
            str(product_ids[j])
        reserve(product_url, product_ids[j], -1 * quantities[j])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
