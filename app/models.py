from app import db, ma
class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    roll_no = db.Column(db.Integer, unique=True)

    def __init__(self, name, roll_no):
        self.name = name
        self.roll_no = roll_no


class StudentSchemaClass(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'roll_no')

StudentSchema = StudentSchemaClass()
StudentsSchema = StudentSchemaClass(many=True)
