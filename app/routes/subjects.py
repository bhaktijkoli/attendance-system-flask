from flask import request, jsonify
from app import app, db
from app.models import Subject, SubjectSchema, SubjectsSchema

@app.route('/subjects', methods=['get'])
def subjects_get():
    subjects = Subject.query.all()
    return SubjectsSchema.jsonify(subjects)

@app.route('/subjects', methods=['post'])
def subjects_post():
    name = request.json['name']
    subject = Subject(name)
    db.session.add(subject)
    db.session.commit()
    return SubjectSchema.jsonify(subject)
