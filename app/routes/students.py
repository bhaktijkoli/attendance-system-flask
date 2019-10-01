from flask import jsonify
from app import app
from app.models import Student, StudentSchema, StudentsSchema
@app.route('/students')
def getStudents():
    students = Student.query.all()
    return StudentsSchema.jsonify(students)
