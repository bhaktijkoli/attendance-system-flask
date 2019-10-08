from flask import request, jsonify
from app import app, db
from app.models import Student, StudentSchema, StudentsSchema
from app.models import Subject
from app.models import Attendance
from app.models import StudentAddendance
import face_recognition
import numpy as np
import os
import time
import datetime
import secrets
from PIL import Image, ImageDraw

@app.route('/attendance', methods=['get'])
def attendance_get():
    student = Student.query.get(1)
    subject = Subject.query.get(1)
    attendance = Attendance(subject=subject, taken_at=datetime.datetime.utcnow())
    db.session.add(attendance)
    student_attendance = StudentAddendance(student=student, attendance=attendance)
    db.session.add(student_attendance)
    db.session.commit();
    return "Ok"

@app.route('/attendance/add', methods=['get'])
def attendance_add():
    return attendance_post()

@app.route('/attendance', methods=['post'])
def attendance_post():
    subjectid = request.form['subject']
    date = request.form['date']
    print(date)
    # LOAD MODEL DATA
    known_face_encodings = np.load(os.path.join(app.config['DATA_FOLDER'], "face_encodings.npy"))
    known_face_ids = np.load(os.path.join(app.config['DATA_FOLDER'], "face_ids.npy"))
    print("Model Loaded", time.process_time())

    # LOAD IMAGE FILE
    imageFile = "test/test.jpg"
    if 'image' in request.files:
        image = request.files['image']
        imageFile = os.path.join(app.config['PUBLIC_FOLDER'], 'attendance', secrets.token_hex(5) + '.jpg')
        image.save(imageFile)

    # LOAD IMAGE DATA
    unknown_image = face_recognition.load_image_file(imageFile)

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    print("Image Loaded", time.process_time())


    pil_image = Image.fromarray(unknown_image)
    draw = ImageDraw.Draw(pil_image)

    # IDENTIFICATION
    attendees_ids = [];
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.54)

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            id = known_face_ids[best_match_index]
            if not id in attendees_ids:
                attendees_ids.append(id)
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    print("Identification done", time.process_time())

    del draw
    pil_image.save('last_result.jpg')

    # CREATE ATTENDANCE
    students = Student.query.all()

    subject = Subject.query.get(subjectid)
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    attendance = Attendance(subject=subject, date=date.date())
    db.session.add(attendance)

    for student in students:
        present = 0
        if student.id in attendees_ids:
            present = 1
        student_attendance = StudentAddendance(student=student, attendance=attendance, present=present)
        db.session.add(student_attendance)

    db.session.commit()
    print("Attendance created", time.process_time())

    return "Ok"
