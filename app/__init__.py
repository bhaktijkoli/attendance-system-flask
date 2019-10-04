from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# MA
ma = Marshmallow(app)

# CONFIG
app.config['PUBLIC_FOLDER'] = "public"

# ROUTES
from app.routes import index
from app.routes import students

db.create_all()
