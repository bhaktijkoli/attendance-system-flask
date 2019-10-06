from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import numpy as np
import os

app = Flask(__name__)

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# MA
ma = Marshmallow(app)

# CONFIG
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['PUBLIC_FOLDER'] = os.path.join('app','static','public')
app.config['DATA_FOLDER'] = "data"

# ROUTES
from app.routes import index
from app.routes import students
from app.routes import train

# CREATE EMPTY MODEL
if not os.path.exists(app.config['DATA_FOLDER']):
    os.mkdir(app.config['DATA_FOLDER'])
    known_face_encodings = []
    known_face_names = []
    np.save(os.path.join(app.config['DATA_FOLDER'], "face_encodings.npy"), np.asarray(known_face_encodings))
    np.save(os.path.join(app.config['DATA_FOLDER'], "face_names.npy"), np.asarray(known_face_names))
    print("Created empty models")

db.create_all()
