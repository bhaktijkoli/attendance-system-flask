from flask import request, jsonify
from app import app, db
from app.models import Student, StudentSchema, StudentsSchema
import face_recognition
import numpy as np
import os

@app.route('/train/check', methods=['get'])
def train_check():
    known_face_encodings = []
    known_face_names = []
    students = Student.query.all()
    for student in students:
        image = face_recognition.load_image_file(os.path.join(app.config['PUBLIC_FOLDER'], student.image))
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(student.name)

    unknown_image = face_recognition.load_image_file("test/test.jpg")
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.54)

        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        print(name)

    return "Ok"
