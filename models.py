from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
db = SQLAlchemy()

# Professor Class
class Professor(UserMixin, db.Model):
    __tablename__="professors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    gender = db.Column(db.String(6), index=True)
    department = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True)
    birthday = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    courses = relationship("Course", backref="professors")
    posts = relationship("Post", backref="professors")

    def __repr__(self):
        return '<Professor {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_course(self,name,subject,number):
        # Notice that we set the foreign key for the passenger class.
        new_course = Course(name=name, subject=subject, number=number )
        db.session.add(new_course)
        db.session.commit()

# Administrator Class
class Administrator(UserMixin, db.Model):
    __tablename__="administrators"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    gender = db.Column(db.String(6), index=True)
    department = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True)
    birthday = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Administrator {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class_registration_table = db.Table('registration',
    db.Column('student_id', Integer(), ForeignKey('students.id')),
    db.Column('course_id', Integer(), ForeignKey('courses.id'))
)

# Student Class
class Student(UserMixin, db.Model):
    __tablename__= "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    gender = db.Column(db.String(6), index=True)
    year = db.Column(db.String(10), index=True)
    major = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True)
    birthday = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    courses = relationship("Course", secondary=class_registration_table, back_populates="students")

    def __repr__(self):
        return '<Student {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Course Class
class Course (db.Model):
    __tablename__= "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    subject = db.Column(db.String(64), index=True)
    number = db.Column(db.String(8), index=True)
    professor_id = Column(Integer, ForeignKey('professors.id'))
    posts = relationship("Post", backref="courses")
    students = relationship("Student", secondary=class_registration_table, back_populates="courses")

# Post Class
class Post(db.Model):
    __tablename__= "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300), unique=False)
    type = db.Column(db.String(20), index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    professor_id = Column(Integer, ForeignKey('professors.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

# Assignment class
class Assignment(db.Model):
    __tablename__= "assignments"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300), unique=False)
    type = db.Column(db.String(20), index=True, unique=False)
    total = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    course_id = Column(Integer, ForeignKey('courses.id'))

# Submission class
class Submission(db.Model):
    __tablename__= "submissions"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    points = db.Column(db.Integer)
    student_id = Column(Integer, ForeignKey('students.id'))
    assign_id = Column(Integer, ForeignKey('assignments.id'))
    assign_total = Column(Integer, ForeignKey('assignments.total'))
    assign_type = Column(String, ForeignKey('assignments.type'))
