import os
import time
import sys
import ssl

import pika

params = pika.ConnectionParameters(
    host=os.environ.get("rabbitmq_host"),
    port=os.environ.get("rabbitmq_port"))

if os.environ.get("stage") == "production":
    creds = pika.PlainCredentials(
        username=os.environ.get("rabbitmq_username"),
        password=os.environ.get("rabbitmq_password"))
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    params = pika.ConnectionParameters(
        host=os.environ.get("rabbitmq_host"),
        port=os.environ.get("rabbitmq_port"),
        virtual_host="/", credentials=creds,
        ssl_options=pika.SSLOptions(ctx))


print("Connecting...")
start_time = time.time()

while True:
    try:
        cnx = pika.BlockingConnection(params)
        break
    except pika.exceptions.AMQPConnectionError:
        if time.time() - start_time > 20:
            sys.exit(1)

print("Connected!")
channel = cnx.channel()

exch_name = "notifications.topic"
channel.exchange_declare(
    exchange=exch_name, exchange_type="topic", durable=True)

queue_name = "Book_Price_Drop"
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(
    exchange=exch_name, queue=queue_name, routing_key="book.#")
cnx.close()
