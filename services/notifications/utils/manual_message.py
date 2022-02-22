import json

import pika

cnx = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672))
channel = cnx.channel()

exch_name = "notifications.topic"
channel.exchange_declare(
    exchange=exch_name, exchange_type="topic", durable=True)

queue_name = "Customer_Notifications"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(
    exchange=exch_name, queue=queue_name, routing_key="order.*")

channel.basic_publish(
    exchange=exch_name, routing_key="order.new",
    body=json.dumps(
        {
            "email": "miguel@email.com",
            "data": "Order created!"
        }
    ), properties=pika.BasicProperties(delivery_mode=2))

cnx.close()
