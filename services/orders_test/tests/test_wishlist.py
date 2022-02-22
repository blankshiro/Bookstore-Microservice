import json
import pytest
import requests
import os

BOOKS_URL = 'http://books:5000'
ORDERS_URL = 'http://orders:8084'
PLACE_ORDER_URL = 'http://place-order:5001'
USERS_URL = 'http://users:8083'
WISHLIST_URL = 'http://wishlist:5000'
SAVE_WISHLIST_URL = 'http://save-wishlist:5000'

def test_health_users():
    result = requests.get(USERS_URL +'/users')
    assert result.status_code == 200

def test_health_wishlist():
    result = requests.get(WISHLIST_URL +'/health')
    assert result.status_code == 200

def test_health_books():
    result = requests.get(BOOKS_URL +'/health')
    assert result.status_code == 200

def test_health_savewishlist():
    result = requests.get(SAVE_WISHLIST_URL +'/health')
    assert result.status_code == 200

def test_save_wishlist():
    wishlistbody =  { 
        "user_id": 1, 
        "wishlist_books" : [{ "book_id":1 }] 
    }
    
    result = requests.post(SAVE_WISHLIST_URL + '/save-wishlist', json = wishlistbody)
    print(result.text)
    assert result.status_code == 201