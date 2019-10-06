from flask import request, jsonify
from app import app, db
from app.models import Student, StudentSchema, StudentsSchema
import face_recognition
import numpy as np
import os
import time

from PIL import Image, ImageDraw

@app.route('/train', methods=['get'])
def train():
    known_face_encodings = []
    known_face_names = []
    students = Student.query.all()
    print("Students Loaded", time.process_time())
    for student in students:
        image = face_recognition.load_image_file(os.path.join(app.config['PUBLIC_FOLDER'], student.image))
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(student.name)

    print("Students Loaded", time.process_time())

    known_face_encodings = np.asarray(known_face_encodings)
    known_face_names = np.asarray(known_face_names)

    file = os.path.join(app.config['DATA_FOLDER'], "face_encodings.npy")
    np.save(file, known_face_encodings)
    file = os.path.join(app.config['DATA_FOLDER'], "face_names.npy")
    np.save(file, known_face_names)
    return "Ok"

@app.route('/train/check', methods=['get'])
def train_check():
    file = os.path.join(app.config['DATA_FOLDER'], "face_encodings.npy")
    known_face_encodings = np.load(file)
    file = os.path.join(app.config['DATA_FOLDER'], "face_names.npy")
    known_face_names = np.load(file)
    print("Model Loaded", time.process_time())

    students = Student.query.all()
    print("Students Loaded", time.process_time())


    unknown_image = face_recognition.load_image_file("test/test.jpg")

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    print("Image Loaded", time.process_time())

    attendees = [];

    # pil_image = Image.fromarray(unknown_image)
    # draw = ImageDraw.Draw(pil_image)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.54)

        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            attendees.append(name)
            # draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        print(name)

    # del draw
    # pil_image.save('test.jpg')
    return str(attendees)
