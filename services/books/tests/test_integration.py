import json
import pytest

def call(client, path, method="GET", body=None):
    mimetype = "application/json"
    headers = {
        "Content-Type": mimetype,
        "Accept": mimetype
    }

    if method == "POST":
        response = client.post(
            path, data=json.dumps(body), headers=headers)
    elif method == "PUT":
        response = client.put(
            path, data=json.dumps(body), headers=headers)
    elif method == "PATCH":
        response = client.patch(
            path, data=json.dumps(body), headers=headers)
    elif method == "DELETE":
        response = client.delete(path)
    else:
        response = client.get(path)

    return {
        "json": json.loads(response.data.decode("utf-8")),
        "code": response.status_code
    }

@pytest.mark.dependency()
def test_health(client):
    result = call(client, "health")
    assert result["code"] == 200

@pytest.mark.dependency()
def test_get_all(client):
    result = call(client, "products")
    assert result["code"] == 200
    assert result["json"]["data"]["books"] == [
        {
            "author": "Ernest Hemingway",
            "book_id": 1,
            "isbn": "0684801221",
            "price": 20,
            "publisher": "Scribner Paperback Fiction",
            "stock": 500,
            "title": "The Old Man and The Sea"
        },
        {
            "author": "Charles Dickens",
            "book_id": 2,
            "isbn": "1411433238",
            "price": 70,
            "publisher": "Barnes & Noble Classics",
            "stock": 45,
            "title": "A Tale of Two Cities"
        },
        {
            "author": "Alexandre Dumas",
            "book_id": 4,
            "isbn": "0140449266",
            "price": 85,
            "publisher": "Penguin Classics",
            "stock": 95,
            "title": "The Count of Monte Cristo"
        }
    ]

@pytest.mark.dependency(depends=["test_get_all"])
def test_get_one_valid(client):
    result = call(client, "products/2")
    assert result["code"] == 200
    assert result["json"]["data"] == {
        "author": "Charles Dickens",
        "book_id": 2,
        "isbn": "1411433238",
        "price": 70,
        "publisher": "Barnes & Noble Classics",
        "stock": 45,
        "title": "A Tale of Two Cities"
    }

@pytest.mark.dependency(depends=["test_get_all"])
def test_get_one_invalid(client):
    result = call(client, "products/10")
    assert result["code"] == 404
    assert result["json"] == {
        "message": "Book not found."
    }

@pytest.mark.dependency(depends=["test_get_all"])
def test_replace_existing_book(client):
    book = {
        "author": "David Kopec",
        "isbn": "1617295981",
        "price": 100,
        "publisher": "Manning Publications",
        "stock": 25,
        "title": "Classic Computer Science Problems in Python"
    }
    result = call(client, "products/2", "PUT", book)
    assert result["code"] == 200
    assert result["json"]["data"] == {
        "book_id": 2, **book
    }

@pytest.mark.dependency(depends=["test_get_all"])
def test_update_existing_book(client):
    book = {
        "author": "Ernest Hemingway",
        "isbn": "0684801221",
        "price": 25,
        "publisher": "Scribner Paperback Fiction",
        "stock": 420,
        "title": "The Old Man and The Sea"
    }
    result = call(client, "products/1", "PATCH", {
        "price": 25,
        "stock": 420
    })
    assert result["code"] == 200
    assert result["json"]["data"] == {
        "book_id": 1, **book
    }

@pytest.mark.dependency(depends=["test_get_all"])
def test_reserve_existing_book(client):
    result = call(client, "products/1", "PATCH", {
        "reserve": 30
    })
    assert result["code"] == 200
    assert result["json"]["data"] == {
        "author": "Ernest Hemingway",
        "book_id": 1,
        "isbn": "0684801221",
        "price": 20,
        "publisher": "Scribner Paperback Fiction",
        "stock": 470,
        "title": "The Old Man and The Sea"
    }

@pytest.mark.dependency(depends=["test_reserve_existing_book"])
def test_unreserve_existing_book(client):
    result = call(client, "products/1", "PATCH", {
        "reserve": -100
    })
    assert result["code"] == 200
    assert result["json"]["data"] == {
        "author": "Ernest Hemingway",
        "book_id": 1,
        "isbn": "0684801221",
        "price": 20,
        "publisher": "Scribner Paperback Fiction",
        "stock": 600,
        "title": "The Old Man and The Sea"
    }

@pytest.mark.dependency(depends=["test_reserve_existing_book"])
def test_reserve_existing_book_fail(client):
    result = call(client, "products/1", "PATCH", {
        "reserve": 505
    })
    assert result["code"] == 500

@pytest.mark.dependency(depends=["test_get_all"])
def test_delete_existing_book(client):
    result = call(client, "products/4", "DELETE")
    assert result["code"] == 200
    assert result["json"]["data"] == {
        "book_id": 4
    }

@pytest.mark.dependency(depends=["test_delete_existing_book"])
def test_get_deleted_book(client):
    test_delete_existing_book(client)
    result = call(client, "products/4")
    assert result["code"] == 404
    assert result["json"] == {
        "message": "Book not found."
    }

@pytest.mark.dependency(depends=["test_get_all"])
def test_create_no_body(client):
    result = call(client, "products", "POST", {})
    assert result["code"] == 500

@pytest.mark.dependency(depends=["test_create_no_body"])
def test_create_new_book(client):
    book = {
        "author": "J R R Tolkien",
        "isbn": "0547928210",
        "price": 70,
        "publisher": "Allen & Unwin",
        "stock": 35,
        "title": "The Fellowship of the Ring"
    }
    result = call(client, "products", "POST", book)
    assert result["code"] == 201
    assert result["json"]["data"] == {
        "book_id": 6, **book
    }

@pytest.mark.dependency(depends=["test_create_new_book"])
def test_replace_new_book(client):
    test_create_new_book(client)
    book = {
        "author": "David Kopec",
        "isbn": "1617295981",
        "price": 100,
        "publisher": "Manning Publications",
        "stock": 25,
        "title": "Classic Computer Science Problems in Python"
    }
    result = call(client, "products/6", "PUT", book)
    assert result["code"] == 200
    assert result["json"]["data"] == {
        "book_id": 6, **book
    }

@pytest.mark.dependency(depends=["test_create_new_book"])
def test_update_new_book(client):
    test_create_new_book(client)
    book = {
        "author": "J R R Tolkien",
        "isbn": "0544003415",
        "price": 70,
        "publisher": "Allen & Unwin",
        "stock": 35,
        "title": "The Lord of the Rings"
    }
    result = call(client, "products/6", "PATCH", {
        "isbn": "0544003415",
        "title": "The Lord of the Rings"
    })
    assert result["code"] == 200
    assert result["json"]["data"] == {
        "book_id": 6, **book
    }

@pytest.mark.dependency(depends=["test_create_new_book"])
def test_delete_new_book(client):
    test_create_new_book(client)
    result = call(client, "products/6", "DELETE")
    assert result["code"] == 200
    assert result["json"]["data"] == {
        "book_id": 6
    }
