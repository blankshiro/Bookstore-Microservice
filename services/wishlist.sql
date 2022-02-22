CREATE DATABASE IF NOT EXISTS wishlist;

use wishlist;

DROP TABLE IF EXISTS wishlist;

CREATE TABLE item (
    item_id int NOT NULL AUTO_INCREMENT,
    user_id int NOT NULL,
    book_id int NOT NULL,
    PRIMARY KEY (item_id)
) AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;