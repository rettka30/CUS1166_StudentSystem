import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import *
from forms import LoginForm, PasswordForm, GPAForm, CreateStudentForm, GPAPForm
from flask_login import current_user, LoginManager, login_user, login_required
from flask_bootstrap import Bootstrap
from scrape import *
import datetime, pygal

app = Flask(__name__)
app.config.from_object(Config)

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

db.init_app(app)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index/<type>/<int:id>')
def index(type, id):
    if type == "Student":
        student = Student.query.get(id)
        courses = student.courses
        return render_template('student_index.html', student=student, courses=courses)
    elif type == "Professor":
        professor = Professor.query.get(id)
        courses = professor.courses
        return render_template('professor_index.html', professor=professor, courses=courses)
    elif type == "Administrator":
        admin = Administrator.query.get(id)
        return render_template('admin_index.html', admin=admin)
    else:
        return render_template('error.html')

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

@app.route('/login/<type>', methods=['GET','POST'])
def login(type):
    if type == "Student":
        if current_user.is_authenticated:
            return redirect(url_for('index', type="Student", id=form.id.data))
        form = LoginForm()
        if form.validate_on_submit():
            user = Student.query.filter_by(id=form.id.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid id or password')
                return redirect(url_for('login', type='Student'))
            return redirect(url_for('index', type="Student", id=form.id.data))
        return render_template('login.html', form=form)
    elif type == "Professor":
        if current_user.is_authenticated:
            return redirect(url_for('index', type="Professor", id=form.id.data))
        form = LoginForm()
        if form.validate_on_submit():
            user = Professor.query.filter_by(id=form.id.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid id or password')
                return redirect(url_for('login', type='Professor'))
            return redirect(url_for('index', type="Professor", id=form.id.data))
        return render_template('login.html', form=form)
    else:
        if current_user.is_authenticated:
            return redirect(url_for('index', type="Administrator", id=form.id.data))
        form = LoginForm()
        if form.validate_on_submit():
            user = Administrator.query.filter_by(id=form.id.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid id or password')
                return redirect(url_for('login', type='Administrator'))
            return redirect(url_for('index', type="Administrator", id=form.id.data))
        return render_template('login.html', form=form)

@app.route("/gradebook")
def gradebook():
    pass

@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    # Get information from the form.
    form = CreateStudentForm()
    # Get information from the form.
    if form.validate_on_submit():
        student_name = form.student_name.data
        student_gender = form.student_gender.data
        student_year = form.student_year.data
        student_email = form.student_email.data
        t = form.student_birthday.data
        student_birthday = t.strftime('%m/%d/%Y')
        student_major = form.student_major.data
        student_phone = str(form.student_phone.data)
        b1=student_birthday[:2]
        b2=student_birthday[3:5]
        b3=student_birthday[6:10]
        student_password=b1+b2+b3
        student = Student(name=student_name, gender=student_gender, year=student_year, email=student_email, birthday=student_birthday, major=student_major, phone=student_phone)
        student.set_password(student_password)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('student_roster'))
    return render_template('create_student.html', form = form)

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
        p1=pro_birthday[:4]
        p2=pro_birthday[5:7]
        p3=pro_birthday[8:10]
        pro_password=p2+p3+p1
        pro = Professor(name=pro_name, gender=pro_gender, department=pro_department, email=pro_email, birthday=pro_birthday, phone=pro_phone)
        pro.set_password(pro_password)
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
        a1=admin_birthday[:4]
        a2=admin_birthday[5:7]
        a3=admin_birthday[8:10]
        admin_password=a2+a3+a1
        admin = Administrator(name=admin_name, gender=admin_gender, department=admin_department, email=admin_email, birthday=admin_birthday, phone=admin_phone)
        admin.set_password(admin_password)
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
    elif type == "Administrator":
        admin = Administrator.query.get(id)
        db.session.delete(admin)
        db.session.commit()
        return redirect(url_for('administrator_roster'))
    elif type == "Course":
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return redirect(url_for('course_list'))
    else:
        return render_template('error.html')


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
            return redirect(url_for('index', type='Student', id=id))
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
            return redirect(url_for('index', type='Professor', id=id))
        return render_template('prof_edit.html', professor=professor)
    elif type == "Administrator":
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
            return redirect(url_for('index', type='Administrator', id=id))
        return render_template('admin_edit.html', admin=admin)
    elif type == "Course":
        course = Course.query.get(id)
        if request.method == 'POST':
            course.subject = request.form.get('course_subject')
            course.number = request.form.get('course_number')
            course.name = request.form.get('course_name')
            db.session.add(course)
            db.session.commit()
            return redirect(url_for('details', type='Course', id=id))
        return render_template('course_edit.html', course=course)
    else:
        return render_template('error.html')

@app.route('/details/<type>/<int:id>')
def details(type, id):
    if type == "Student":
        student = Student.query.get(id)
        graph_data = barchart_generator(Student)
        return render_template('students_details.html', student=student, graph_data=graph_data)
    elif type == "Professor":
        prof = Professor.query.get(id)
        return render_template('professor_details.html', prof=prof)
    elif type == "Administrator":
        admin = Administrator.query.get(id)
        return render_template('administrator_details.html', admin=admin)
    elif type == "Course":
        course = Course.query.get(id)
        professor = Professor.query.get(course.professor_id)
        return render_template('course_details.html', course=course, professor=professor)
    else:
        return render_template('error.html')

#Creates Courses
@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    # Get information from the form.
    professors = Professor.query.all()
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_subject = request.form.get('course_subject')
        course_number = request.form.get('course_number')
        professor_name = request.form.get('professor_name')
        professor = Professor.query.filter_by(name=professor_name).first()
        professor_id = professor.id
        course = Course(name=course_name, subject=course_subject, number=course_number, professor_id=professor_id)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('course_list'))
    return render_template('create_course.html', professors=professors)

@app.route('/course_list')
def course_list():
    courses = Course.query.all()
    return render_template('course_list.html', courses=courses)

@app.route('/change_password/<type>/<int:id>',methods=['GET','POST'])
def change_password(type, id):
    if type == "Student":
        user = Student.query.get(id)
        # if user.is_authenticated:
        #     return redirect(url_for('index', type="Student", id=id))
        form = PasswordForm()
        if form.validate_on_submit():
            if user is None or not user.check_password(form.password.data):
                    flash('Invalid password')
                    return redirect(url_for('change_password', type='Student', id=id))
            user.set_password(form.np.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index', type='Student', id=id))
        return render_template('student_password.html', form=form)
    elif type == "Professor":
        user = Professor.query.get(id)
        # if user.is_authenticated:
        #     return redirect(url_for('index', type="Student", id=id))
        form = PasswordForm()
        if form.validate_on_submit():
            if user is None or not user.check_password(form.password.data):
                    flash('Invalid password')
                    return redirect(url_for('change_password', type='Professor', id=id))
            user.set_password(form.np.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index', type='Professor', id=id))
        return render_template('prof_password.html', form=form)
    elif type == "Administrator":
        user = Administrator.query.get(id)
        # if user.is_authenticated:
        #     return redirect(url_for('index', type="Student", id=id))
        form = PasswordForm()
        if form.validate_on_submit():
            if user is None or not user.check_password(form.password.data):
                    flash('Invalid password')
                    return redirect(url_for('change_password', type='Administrator', id=id))
            user.set_password(form.np.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index', type='Administrator', id=id))
        return render_template('admin_password.html', form=form)
    else:
        return render_template('error.html')


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
    result1=0
    form = GPAForm()
    form1 = GPAPForm()
    GPA_chart = pygal.Bar()
    GPA_chart2 = pygal.Radar()
    graph_data = GPA_chart.render_data_uri()
    graph_data2 = GPA_chart2.render_data_uri()
    # Get information from the form.
    if form.validate_on_submit():
        grades = form.current_grades.data
        # = request.form.get('student_gender')
        result = gpa_calculater(grades)
    if form1.validate_on_submit():
        current_GPA = form1.current_GPA.data
        Num_of_course = form1.Num_of_course.data
        future_grades = form1.future_grades.data
        # = request.form.get('student_gender')
        result1 = gpa_predictor(current_GPA, Num_of_course, future_grades)
    if result != 0:
        grades = a_4(grades)
        GPA_chart.title = "GPA Chart"
        GPA_chart.y_labels = [
            {'label': 'A', 'value': 4.0},
            {'label': 'A-', 'value': 3.7},
            {'label': 'B+', 'value': 3.3},
            {'label': 'B', 'value': 3.0},
            {'label': 'B-', 'value': 2.7},
            {'label': 'C+', 'value': 2.3},
            {'label': 'C', 'value': 2.0},
            {'label': 'C-', 'value': 1.7},
            {'label': 'D+', 'value': 1.3},
            {'label': 'D', 'value': 1.0},
            {'label': 'D-', 'value': 0.7},
            {'label': 'F', 'value': 0}]
        GPA_chart2.add("grades",grades)
        for element in grades:
            GPA_chart.add('', element)

        graph_data = GPA_chart.render_data_uri()
        graph_data2 = GPA_chart2.render_data_uri()

    return render_template('gpa.html', graph_data = graph_data, graph_data2 = graph_data2, result = result, form = form, form1 = form1, result1 =result1)

def gpa_predict(current_grades,times, future_grades):
    gpa_dict = {'F': 0, 'D-': 0.7, 'D': 1.0, 'D+': 1.3, 'C-': 1.7, 'C': 2.0, 'C+': 2.3, 'B-': 2.7, 'B': 3.0, 'B+': 3.3, 'A-': 3.7, 'A': 4.0, 'A+': 4.0}
    total = current_grades*times
    grades=future_grades.upper().split(",")
    numOfCourses=len(grades)
    for element in grades:
        total += gpa_dict[element]
    gpa = total / (numOfCourses+times)
    return gpa

def a_4(a):
    gpa_dict = {'F': 0, 'D-': 0.7, 'D': 1.0, 'D+': 1.3, 'C-': 1.7, 'C': 2.0, 'C+': 2.3, 'B-': 2.7, 'B': 3.0, 'B+': 3.3, 'A-': 3.7, 'A': 4.0, 'A+': 4.0}
    grades=a.upper().split(",")
    grades_m = []
    for element in grades:
        grades_m.append(gpa_dict[element])
    return grades_m

def gpa_predictor(current_grades,times, future_grades):
    try:
        return round(gpa_predict(current_grades,times, future_grades),2)
    except:
        return 'please enter in the right form'

def barchart_generator(Student):
    GPA_chart = pygal.Bar()
    graph_data = GPA_chart.render_data_uri()
    grades = a_4("a,a-,b,b+")
    GPA_chart.title = "GPA Chart"
    GPA_chart.y_labels = [
        {'label': 'A', 'value': 4.0},
        {'label': 'A-', 'value': 3.7},
        {'label': 'B+', 'value': 3.3},
        {'label': 'B', 'value': 3.0},
        {'label': 'B-', 'value': 2.7},
        {'label': 'C+', 'value': 2.3},
        {'label': 'C', 'value': 2.0},
        {'label': 'C-', 'value': 1.7},
        {'label': 'D+', 'value': 1.3},
        {'label': 'D', 'value': 1.0},
        {'label': 'D-', 'value': 0.7},
        {'label': 'F', 'value': 0}]
    for element in grades:
        GPA_chart.add('', element)
    graph_data = GPA_chart.render_data_uri()
    return graph_data
