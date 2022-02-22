import json
import pytest
import requests
import os
import mysql.connector
import time
from urllib.parse import urlparse

BOOKS_URL = 'http://books:5000'
USERS_URL = 'http://users:8083'
WISHLIST_URL = 'http://wishlist:5000'

# product, monitorprice, wishlist, notification, users

def test_health_users():
    result = requests.get(USERS_URL +'/users')
    assert result.status_code == 200

def test_health_wishlist():
    result = requests.get(WISHLIST_URL +'/health')
    assert result.status_code == 200

def test_health_books():
    result = requests.get(BOOKS_URL +'/health')
    assert result.status_code == 200

def test_price_drop():
    db_url = urlparse(os.environ.get("db_conn_notification"))
    data_size = 0
    try:
        cnx = mysql.connector.connect(
            user=db_url.username,
            password=db_url.password,
            host=db_url.hostname,
            port=db_url.port,
            database="notification")
        
        cursor = cnx.cursor()
        cursor.execute("""SELECT * FROM NOTIFICATION;""")
        data_size = len(cursor)
        cnx.close()

    except mysql.connector.Error as err:
        print("sql error")

    pricedrop = {
        "price": 1.0, 
    }

    pricedropresult = requests.patch(BOOKS_URL + '/products/1', json=pricedrop)
    assert pricedropresult.status_code == 200

    time.sleep(10)
    try:
        cnx = mysql.connector.connect(
            user=db_url.username,
            password=db_url.password,
            host=db_url.hostname,
            port=db_url.port,
            database="notification")
        
        cursor = cnx.cursor()
        cursor.execute("""SELECT * FROM NOTIFICATION;""")
        assert data_size + 1 == len(cursor) 
        cnx.close()
        
    except mysql.connector.Error as err:
        print("sql error")

    


