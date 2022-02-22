CREATE DATABASE IF NOT EXISTS notification;

use notification;

DROP TABLE IF EXISTS notification;

CREATE TABLE notification (
    id int NOT NULL AUTO_INCREMENT,
    email varchar(64) NOT NULL,
    data varchar(256) NOT NULL,
    PRIMARY KEY (id)
) AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;