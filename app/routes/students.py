from flask import request, jsonify
from app import app, db
from app.models import Student, StudentSchema, StudentsSchema
@app.route('/students', methods=['get'])
def students_get():
    students = Student.query.all()
    return StudentsSchema.jsonify(students)

@app.route('/students', methods=['post'])
def students_post():
    name = request.json['name']
    roll_no = request.json['roll_no']
    student = Student(name, roll_no)
    db.session.add(student)
    db.session.commit()
    return StudentSchema.jsonify(student)
