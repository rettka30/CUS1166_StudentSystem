import sys
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import *

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    # Get information from the form.
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_gender = request.form['student_gender']
        student_year = request.form.get('student_year')
        student_email = str(request.form.get('student_email'))
        student_birthday = str(request.form.get('student_birthday'))
        student_major = request.form.get('student_major')
        student_phone = str(request.form.get('student_phone'))
        student = Student(name=student_name, gender=student_gender, year=student_year, email=student_email, birthday=student_birthday, major=student_major, phone=student_phone)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_student.html')

@app.route('/delete/<int:student_id>')
def delete(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:student_id>', methods=['GET, POST'])
def edit(student_id):
    pass

@app.route('/student/<int:student_id>')
def student(student_id):
    student = Student.query.get(student_id)
    return render_template('students_details.html', student=student)

#Creates Courses
@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    # Get information from the form.
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_subject = request.form.get('course_subject')
        course_number = request.form.get('course_number')
        course = Course(course_name=course_name, course_subject=course_subject, course_number=course_number)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_course.html')

def main():
    if (len(sys.argv)==2):
        print(sys.argv)
        if sys.argv[1] == 'createdb':
            db.create_all()
    else:
        print("Run app using 'flask run")
        print("To create a database use 'python app.py createdb")

if __name__ == "__main__":
    with app.app_context():
        main()
