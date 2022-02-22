import os
import json
from urllib.parse import urlparse

import mysql.connector

import amqp_setup
import ses_script

db_url = urlparse(os.environ.get("db_conn_notifications"))


def callback(channel, method, properties, body):
    message_body = json.loads(body)
    email = message_body["email"]
    data = json.dumps(message_body["data"])
    log_data = data.replace("\n", "")

    try:
        cnx = mysql.connector.connect(
            user=db_url.username,
            password=db_url.password,
            host=db_url.hostname,
            port=db_url.port,
            database="notification")
        cnx.cursor().execute("""INSERT INTO notification
    (email, data) VALUES (%s, %s);""", (email, data))
        cnx.commit()
        cnx.close()
        print(f"SUCCESS,{email},{log_data}\n")
    except mysql.connector.Error as err:
        print(f"FAIL,{email},{log_data},{err}\n")

    # Invoke Amazon SES to send email
    ses_script.EmailSender().send_email(
        sender="wjtay1998@gmail.com",
        recipient=email,
        subject="Notification",
        body_text=data,
        body_html=f"""\
<html>
  <head></head>
  <body>
    <h3>Notification</h3>
    <p>The following data was received by the notifications microservice:</p>
    <code>{data}</code>
  </body>
</html>""")


amqp_setup.channel.basic_consume(
    queue=amqp_setup.queue_name,
    on_message_callback=callback, auto_ack=True)
amqp_setup.channel.start_consuming()
