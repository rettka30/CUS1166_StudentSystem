from flask_sqlalchemy import SQLAlchemy
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_user import UserManager, UserMixin, PasswordManager
from datetime import datetime
db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    uniqueid = db.Column(db.String(5), index=True)
    name = db.Column(db.String(120), index=True, unique=False)
    gender = db.Column(db.String(6), index=True)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(120), index=True)
    birthday = db.Column(db.String(120), index=True)
    active = db.Column(db.Boolean())
    roles = relationship("Role", secondary="user_roles")
    password = db.Column(db.String(128))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=False)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id'))

class_registration_table = db.Table('registration',
    db.Column('student_id', Integer, ForeignKey('students.id')),
    db.Column('course_id', Integer, ForeignKey('courses.id'))
)

# Student Class; Inheirits User, UserMixin,
class Student(User, db.Model):
    __tablename__= "students"
    id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    year = db.Column(db.String(10), index=True)
    major = db.Column(db.String(120), index=True)
    courses = relationship("Course", secondary=class_registration_table, back_populates="students")
    submissions = relationship("Submission", backref="students")
    posts = relationship("Post", backref="students")

    def __repr__(self):
        return '<Student {}>'.format(self.id)

# Professor Class, Inheirits User
class Professor(User, db.Model):
    __tablename__="professors"
    id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    department = db.Column(db.String(120), index=True)
    courses = relationship("Course", backref="professors")
    posts = relationship("Post", backref="professors")

    def __repr__(self):
        return '<Professor {}>'.format(self.id)

# Administrator Class, Inheirits User
class Administrator(User, db.Model):
    __tablename__="administrators"
    id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    department = db.Column(db.String(120), index=True)

    def __repr__(self):
        return '<Administrator {}>'.format(self.id)

# Course Class
class Course (db.Model):
    __tablename__= "courses"
    id = db.Column(db.Integer, primary_key=True)
    uniqueid = db.Column(db.String(5), index=True)
    name = db.Column(db.String(120), index=True, unique=False)
    subject = db.Column(db.String(64), index=True)
    number = db.Column(db.String(8), index=True)
    day = db.Column(db.String(10), index=True)
    start_time = db.Column(db.Time, index=True)
    end_time = db.Column(db.Time, index=True)
    professor_id = Column(Integer, ForeignKey('professors.id'))
    posts = relationship("Post", backref="courses")
    assignments = relationship("Assignment", backref="courses")
    students = relationship("Student", secondary=class_registration_table, back_populates="courses")

# Post Class
class Post(db.Model):
    __tablename__= "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300), unique=False)
    type = db.Column(db.String(20), index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    professor_id = Column(Integer, ForeignKey('professors.id'))
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

# Assignment class
class Assignment(db.Model):
    __tablename__= "assignments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=False)
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
    assign_course_id = Column(Integer, ForeignKey('assignments.course_id'))
    # assign_type = Column(String, ForeignKey('assignments.type'))

    def set_grade(self, grade):
        self.points = grade

#Unique ID Class
class Unique(db.Model):
    __tablename__= "unique"
    prefix = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
