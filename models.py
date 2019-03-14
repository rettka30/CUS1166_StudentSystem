from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Student Class
class Student(db.Model):
    __tablename__= "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    gender = db.Column(db.String(64), index=True)

# Professor Class

# Administrator Class

# Course Class
class Course (db.Model):
    __tablename__= "courses"
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), index=True, unique=False)
    course_subject = db.Column(db.String(64), index=True)
    course_number =  = db.Column(db.String(8), index=True)
