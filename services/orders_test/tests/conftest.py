# import pytest

# @pytest.fixture
# def client():
#     from src import app
#     app.db.engine.execute("DROP TABLE IF EXISTS product;")
#     app.db.engine.execute("""\
# CREATE TABLE product (
#     book_id int NOT NULL AUTO_INCREMENT,
#     title varchar(64) NOT NULL,
#     isbn varchar(16) NOT NULL,
#     author varchar(32) NOT NULL,
#     publisher varchar(32) NOT NULL,
#     price float NOT NULL,
#     stock int NOT NULL,
#     PRIMARY KEY (book_id)
# ) AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;""")
#     app.db.engine.execute("""\
# INSERT INTO product VALUES
#     (1, 'The Old Man and The Sea', '0684801221', 'Ernest Hemingway',
#         'Scribner Paperback Fiction', 20, 500),
#     (2, 'A Tale of Two Cities', '1411433238', 'Charles Dickens',
#         'Barnes & Noble Classics', 70, 45),
#     (4, 'The Count of Monte Cristo', '0140449266', 'Alexandre Dumas',
#         'Penguin Classics', 85, 95)""")
#     return app.app.test_client()
