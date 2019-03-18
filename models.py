from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
#from flask_login import UserMixin

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
    password_hash = db.Column(db.String(128))

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
    password_hash = db.Column(db.String(128))

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
    password_hash = db.Column(db.String(128))

# Course Class
class Course (db.Model):
    __tablename__= "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    subject = db.Column(db.String(64), index=True)
    number = db.Column(db.String(8), index=True)

#from models.py in microblog to create password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
