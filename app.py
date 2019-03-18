import sys
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from config import Config
from models import *
from forms import LoginForm, GPAForm
from flask_login import current_user, LoginManager, login_user
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

db.init_app(app)
login = LoginManager(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student_roster')
def student_roster():
    students = Student.query.all()
    return render_template('student_roster.html', students=students)

@app.route('/professor_roster')
def professor_roster():
    professors = Professor.query.all()
    return render_template('professor_roster.html', professors=professors)

@app.route('/administrator_roster')
def administrator_roster():
    admins = Administrator.query.all()
    return render_template('administrator_roster.html', admins=admins)

@app.route('/student_login', methods=['GET','POST'])
def student_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(id=form.id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid id or password')
            return redirect(url_for('login'))
        login_user(id, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('student_login.html', title='Student Sign In', form=form)

@app.route('/professor_login', methods=['GET','POST'])
def professor_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Professor.query.filter_by(id=form.id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid id or password')
            return redirect(url_for('login'))
        login_user(id, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('professor_login.html', title='Professor Sign In', form=form)

@app.route('/admin_login', methods= ['GET','POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Administrator.query.filter_by(id=form.id.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid id or password')
            return redirect(url_for('login'))
        login_user(id, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('admin_login.html', title='Administrator Sign In', form=form)

@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
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
        return redirect(url_for('student_roster'))
    return render_template('create_student.html')

@app.route('/create_professor', methods=['GET', 'POST'])
def create_professor():
    # Get information from the form.
    if request.method == 'POST':
        pro_name = request.form.get('professor_name')
        pro_gender = request.form['professor_gender']
        pro_department = request.form.get('professor_department')
        pro_email = str(request.form.get('professor_email'))
        pro_birthday = str(request.form.get('professor_birthday'))
        pro_phone = str(request.form.get('professor_phone'))
        pro = Professor(name=pro_name, gender=pro_gender, department=pro_department, email=pro_email, birthday=pro_birthday, phone=pro_phone)
        db.session.add(pro)
        db.session.commit()
        return redirect(url_for('professor_roster'))
    return render_template('create_professor.html')

@app.route('/create_administrator', methods=['GET', 'POST'])
def create_administrator():
    # Get information from the form.
    if request.method == 'POST':
        admin_name = request.form.get('admin_name')
        admin_gender = request.form['admin_gender']
        admin_department = request.form.get('admin_department')
        admin_email = str(request.form.get('admin_email'))
        admin_birthday = str(request.form.get('admin_birthday'))
        admin_phone = str(request.form.get('admin_phone'))
        admin = Administrator(name=admin_name, gender=admin_gender, department=admin_department, email=admin_email, birthday=admin_birthday, phone=admin_phone)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('administrator_roster'))
    return render_template('create_administrator.html')

@app.route('/delete/<type>/<int:id>')
def delete(type, id):
    if type == "Student":
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('student_roster'))
    elif type == "Professor":
        professor = Professor.query.get(id)
        db.session.delete(professor)
        db.session.commit()
        return redirect(url_for('professor_roster'))
    else:
        admin = Administrator.query.get(id)
        db.session.delete(admin)
        db.session.commit()
        return redirect(url_for('administrator_roster'))


@app.route('/edit/<type>/<int:id>', methods=['GET', 'POST'])
def edit(type, id):
    if type == "Student":
        student = Student.query.get(id)
        if request.method == 'POST':
            student.name = request.form.get('student_name')
            student.gender = request.form['student_gender']
            student.year = request.form.get('student_year')
            student.email = str(request.form.get('student_email'))
            student.birthday = str(request.form.get('student_birthday'))
            student.major = request.form.get('student_major')
            student.phone = str(request.form.get('student_phone'))
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('user_details', type='Student', id=id))
        return render_template('student_edit.html', student=student)
    elif type == "Professor":
        professor = Professor.query.get(id)
        if request.method == 'POST':
            professor.name = request.form.get('professor_name')
            professor.gender = request.form['professor_gender']
            professor.department = request.form.get('professor_department')
            professor.email = str(request.form.get('professor_email'))
            professor.birthday = str(request.form.get('professor_birthday'))
            professor.phone = str(request.form.get('professor_phone'))
            db.session.add(professor)
            db.session.commit()
            return redirect(url_for('user_details', type='Professor', id=id))
        return render_template('prof_edit.html', professor=professor)
    else:
        admin = Administrator.query.get(id)
        if request.method == 'POST':
            admin.name = request.form.get('admin_name')
            admin.gender = request.form['admin_gender']
            admin.department = request.form.get('admin_department')
            admin.email = str(request.form.get('admin_email'))
            admin.birthday = str(request.form.get('admin_birthday'))
            admin.phone = str(request.form.get('admin_phone'))
            db.session.add(admin)
            db.session.commit()
            return redirect(url_for('user_details', type='Administrator', id=id))
        return render_template('admin_edit.html', admin=admin)

@app.route('/user_details/<type>/<int:id>')
def user_details(type, id):
    if type == "Student":
        student = Student.query.get(id)
        return render_template('students_details.html', student=student)
    elif type == "Professor":
        prof = Professor.query.get(id)
        return render_template('professor_details.html', prof=prof)
    else:
        admin = Administrator.query.get(id)
        return render_template('administrator_details.html', admin=admin)

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





def gpa_calculate(grades):
    gpa_dict = {'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1, 'D-': 0.7, 'F': 0}
    total= 0
    grades=grades.upper().split(",")
    numOfCourses=len(grades)
    for element in grades:
        total += gpa_dict[element]
    gpa = total / numOfCourses
    return gpa

def gpa_calculater(grades):
    try:
        return round(gpa_calculate(grades),2)
    except:
        return 'please enter in the right form'

#gpa counter
@app.route('/gpa', methods=['GET', 'POST'])
def gpa():
    result=0
    form = GPAForm()
    # Get information from the form.
    if form.validate_on_submit():
        grades = form.current_grades.data
        # = request.form.get('student_gender')
        result = gpa_calculater(grades)
    return render_template('gpa.html', result = result, form = form)
