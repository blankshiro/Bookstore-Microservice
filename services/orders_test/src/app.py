import os
import json

import pika

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = \
    os.environ.get("db_conn_books") + "/product"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size": 100,
    "pool_recycle": 280
}

db = SQLAlchemy(app)
CORS(app)