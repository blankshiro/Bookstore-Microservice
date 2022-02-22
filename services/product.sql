CREATE DATABASE IF NOT EXISTS product;

use product;

DROP TABLE IF EXISTS product;

CREATE TABLE product (
    book_id int NOT NULL AUTO_INCREMENT,
    title varchar(64) NOT NULL,
    isbn varchar(16) NOT NULL,
    author varchar(32) NOT NULL,
    publisher varchar(32) NOT NULL,
    price float NOT NULL,
    stock int NOT NULL,
    PRIMARY KEY (book_id)
) AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;