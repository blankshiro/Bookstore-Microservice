import json
import pytest
import requests
import os
import time

## Additional delay
time.sleep(60)
# product_service_url = os.environ.get("books_service_url_internal")
# users_service_url = os.environ.get("users_service_url_internal")
# wishlist_service_url = os.environ.get("wishlist_service_url_internal")
# order_service_url = os.environ.get("orders_service_url_internal")
# place_order_service_url = os.environ.get("place_order_service_url_internal")


BOOKS_URL = 'http://books:5000'
ORDERS_URL = 'http://orders:8084'
PLACE_ORDER_URL = 'http://place-order:5001'
USERS_URL = 'http://users:8083'

def test_health_books():
    result = requests.get(BOOKS_URL +'/health')
    assert result.status_code == 200

def test_health_order():
    result = requests.get(ORDERS_URL +'/orders')
    assert result.status_code == 200


def test_create_order():
    userbody = {
        "name":'testuser',
        "email": "testemail@gmail.com"
    }

    userresult = requests.post(USERS_URL + '/users', json = userbody)
    assert userresult.status_code == 201
    print(userresult.text)

    book = {
        "author": "David Kopec",
        "isbn": "1617295981",
        "price": 100,
        "publisher": "Manning Publications",
        "stock": 25,
        "title": "Classic Computer Science Problems in Python"
    }
    result = requests.post(BOOKS_URL + '/products', json = book)
    # print(result.text)
    assert result.status_code == 201
    body = result.json()
    
    assert body["data"] == {
        "book_id": 1, **book
    }

    
    place_order_body = {
        "user_id": 1,
        "product_list":[{"product_id": 1, "quantity": 1}],
        "card_details":{"cardNumber":"4000056655665556", "expiryMonth":12, "expiryYear":2023, "cvv":123}
    }
    result2 = requests.post(PLACE_ORDER_URL + '/createorder', json=place_order_body)
    print('result2')
    print(result2.text)

    assert result2.status_code == 200

def test_delete_order():    
    delete_order_body = {
        "order_id": 1,
    }
    result2 = requests.post(PLACE_ORDER_URL + '/deleteorder', json=delete_order_body)
    print(result2.text)
    assert result2.status_code == 200


