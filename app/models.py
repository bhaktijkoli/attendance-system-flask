from app import db, ma

# STUDENT MODEL
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    roll_no = db.Column(db.Integer, unique=True)
    image = db.Column(db.String(100), unique=True)
    attendances = db.relationship('StudentAddendance', backref="student")

    def __init__(self, name, roll_no, image):
        self.name = name
        self.roll_no = roll_no
        self.image = image


class StudentSchemaClass(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'roll_no', 'image')

StudentSchema = StudentSchemaClass()
StudentsSchema = StudentSchemaClass(many=True)

# SUBJECT MODEL
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    attendances = db.relationship('Attendance', backref="subject")

    def __init__(self, name):
        self.name = name

class SubjectSchemaClass(ma.Schema):
    class Meta:
        fields = ('id', 'name')

SubjectSchema = SubjectSchemaClass()
SubjectsSchema = SubjectSchemaClass(many=True)

# STUDENT ATTENDANCE MODEL
class StudentAddendance(db.Model):
    __tablename__ = 'student_attendances'
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendances.id'))
    present = db.Column(db.Integer, default='0')

class StudentAddendanceSchemaClass(ma.Schema):
    class Meta:
        fields = ('id', 'student', 'present')

    student = ma.Nested(StudentSchema)

StudentAddendanceSchema = StudentAddendanceSchemaClass()
StudentAddendancesSchema = StudentAddendanceSchemaClass(many=True)

# ATTENDANCE MODEL
class Attendance(db.Model):
    __tablename__ = 'attendances'
    id = db.Column(db.Integer, primary_key = True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    date = db.Column(db.Date)
    students = db.relationship('StudentAddendance', backref="attendance")

class AttendanceSchemaClass(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'subject', 'students')

    subject = ma.Nested(SubjectSchema)
    students = ma.Nested(StudentAddendancesSchema)

AttendanceSchema = AttendanceSchemaClass()
AttendancesSchema = AttendanceSchemaClass(many=True)
