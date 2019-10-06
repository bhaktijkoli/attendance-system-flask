from flask import request, jsonify
from app import app, db
from werkzeug.utils import secure_filename
from app.models import Student, StudentSchema, StudentsSchema
import numpy as np
import face_recognition
import secrets
import os

@app.route('/students', methods=['get'])
def students_get():
    students = Student.query.all()
    return StudentsSchema.jsonify(students)

@app.route('/students', methods=['post'])
def students_post():
    name = request.form['name']
    roll_no = request.form['roll_no']
    image = request.files['image']
    filename = secrets.token_hex(5) + '.jpg'
    image.save(os.path.join(app.config['PUBLIC_FOLDER'], filename))
    student = Student(name, roll_no, filename)
    db.session.add(student)
    db.session.commit()
    # IMAGE ENCODING
    image = face_recognition.load_image_file(os.path.join(app.config['PUBLIC_FOLDER'], filename))
    face_encoding = face_recognition.face_encodings(image)[0]
    print(face_encoding)
    # UPDATING DATA MODEL
    file = os.path.join(app.config['DATA_FOLDER'], "face_encodings.npy")
    known_face_encodings = np.load(file).tolist()
    known_face_encodings.append(face_encoding)
    np.save(file, np.asarray(known_face_encodings))
    file = os.path.join(app.config['DATA_FOLDER'], "face_names.npy")
    known_face_names = np.load(file).tolist()
    known_face_names.append(student.name)
    np.save(file, np.asarray(known_face_names))

    return StudentSchema.jsonify(student)
