from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Professor Class
class Professor(db.Model):
    __tablename__="professors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    gender = db.Column(db.String(6), index=True)
    department = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True)
    birthday = db.Column(db.String(120), index=True)

# Administrator Class
class Administrator(db.Model):
    __tablename__="administrators"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    gender = db.Column(db.String(6), index=True)
    department = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True)
    birthday = db.Column(db.String(120), index=True)

# Student Class
class Student(db.Model):
    __tablename__= "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    gender = db.Column(db.String(6), index=True)
    year = db.Column(db.String(10), index=True)
    major = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True)
    birthday = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True)

# Course Class
class Course (db.Model):
    __tablename__= "courses"
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), index=True, unique=False)
    course_subject = db.Column(db.String(64), index=True)
    course_number = db.Column(db.String(8), index=True)
