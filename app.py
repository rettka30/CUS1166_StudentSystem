import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import *
from forms import LoginForm, PasswordForm, CreateStudentForm, CreateProfessorForm, CreateAdministratorForm, CreateAssignment, GPAPForm, RegisterCourseForm
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from flask_bootstrap import Bootstrap
from flask_user import login_required, PasswordManager, UserManager, UserMixin, roles_required
from scrape import *
import datetime, pygal, time
import requests
import urllib.parse
from flask_uploads import UploadSet, configure_uploads, ALL

# app = Flask(__name__)
# app.config.from_object(Config)

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

db.init_app(app)
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'

# Setup Flask-User
user_manager = UserManager(app, db, User)
password_manager = PasswordManager(app)

#Flask-Uploads
files = UploadSet('files', ALL)

app.config['UPLOADED_FILES_DEST'] = 'static/files'
configure_uploads(app, files)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/')
def home():
    flash('a')
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # if session.get('was_once_logged_in'):
    #     # prevent flashing automatically logged out message
    #     del session['was_once_logged_in']
    flash('You have successfully logged yourself out.')
    return redirect(url_for('welcome'))

@app.route('/index/<type>/<int:id>')
@login_required
# @roles_required('<type>')
def index(type, id):
    if type == "Student":
        student = Student.query.get(id)
        courses = student.courses
        submissions = student.submissions
        return render_template('student_index.html', student=student, courses=courses, submissions=submissions)
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
@login_required
@roles_required('Admin')
def student_roster():
    students = Student.query.all()
    return render_template('student_roster.html', students=students)

@app.route('/professor_roster')
@login_required
@roles_required('Admin')
def professor_roster():
    professors = Professor.query.all()
    return render_template('professor_roster.html', professors=professors)

@app.route('/administrator_roster')
# @login_required
# @roles_required('Admin')
def administrator_roster():
    admins = Administrator.query.all()
    return render_template('administrator_roster.html', admins=admins)

@app.route('/login/<type>', methods=['GET','POST'])
@login_required
#@roles_required('<type>')
def login(type):
    if type == "Student":
    #     if current_user.is_authenticated:
    #         return redirect(url_for('index', type="Student", id=form.id.data))
    #     form = LoginForm()
    #     if form.validate_on_submit():
    #         user = Student.query.filter_by(id=form.id.data).first()
    #         if password_manager.verify_password(form.password.data, user.password):
    #             login_user(user)
    #         else:
    #             flash('Invalid id or password')
    #             return redirect(url_for('login', type='Student'))
    #         return redirect(url_for('index', type="Student", id=form.id.data))
    #     return render_template('login.html', form=form)
        return redirect(url_for('index', type="Student", id=current_user.id))
    elif type == "Professor":
        # if current_user.is_authenticated:
        #     return redirect(url_for('index', type="Professor", id=form.id.data))
        # form = LoginForm()
        # if form.validate_on_submit():
        #     user = Professor.query.filter_by(id=form.id.data).first()
        #     if password_manager.verify_password(form.password.data, user.password):
        #         login_user(user)
        #     else:
        #         flash('Invalid id or password')
        #         return redirect(url_for('login', type='Professor'))
        #     return redirect(url_for('index', type="Professor", id=form.id.data))
        # return render_template('login.html', form=form)
        return redirect(url_for('index', type="Professor", id=current_user.id))
    else:
        # if current_user.is_authenticated:
        #     return redirect(url_for('index', type="Administrator", id=form.id.data))
        # form = LoginForm()
        # if form.validate_on_submit():
        #     user = Administrator.query.filter_by(id=form.id.data).first()
        #     if password_manager.verify_password(form.password.data, user.password):
        #         login_user(user)
        #         flash('Successfully login')
        #         return redirect(url_for('index', type="Administrator", id=form.id.data))
        #     else:
        #         flash('Invalid id or password')
        #         return redirect(url_for('login', type='Administrator'))
        # return render_template('login.html', form=form)
        return redirect(url_for('index', type="Administrator", id=current_user.id))

@app.route("/assignment/gradebooks/<int:id>")
@login_required
@roles_required('Professor')
def gradebooks(id):
    course = Course.query.get(id)
    assignments = course.assignments
    return render_template('gradebooks.html', course=course, assignments=assignments)

@app.route("/gradebook/<int:id>", methods=['GET', 'POST'])
@login_required
@roles_required('Professor')
def gradebook(id):
    assignment = Assignment.query.get(id)
    course_id = assignment.course_id
    course = Course.query.get(course_id)
    students = course.students
    submissions = Submission.query.filter_by(assign_id=assignment.id).all()
    if request.method == 'POST':
        id = request.form['id']
        grade = request.form['grade']
        submission = Submission.query.filter_by(student_id=id, assign_id=assignment.id).first()
        submission.set_grade(grade)
        db.session.add(submission)
        db.session.commit()
        return redirect(url_for('gradebook', id=assignment.id))
    return render_template('gradebook.html', assignment=assignment, students=students, submissions=submissions)

@app.route('/create_student', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
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
        student_role = Role(name='Student')
        student_ui = generateuniqueid("Student")
        student_type = "Student"
        student = Student(uniqueid=student_ui, name=student_name, gender=student_gender,
            year=student_year, email=student_email, birthday=student_birthday,
            major=student_major, phone=student_phone, active=True, type=student_type)
        student.password = password_manager.hash_password(student_password)
        student.roles = [student_role,]
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('student_roster'))
    return render_template('create_student.html', form = form)

@app.route('/create_professor', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def create_professor():
    # Get information from the form.
    form = CreateProfessorForm()
    # Get information from the form.
    if form.validate_on_submit():
        professor_name = form.professor_name.data
        professor_gender = form.professor_gender.data
        professor_department = form.professor_department.data
        professor_email = form.professor_email.data
        t = form.professor_birthday.data
        professor_birthday = t.strftime('%m/%d/%Y')
        professor_phone = str(form.professor_phone.data)
        p1=professor_birthday[:2]
        p2=professor_birthday[3:5]
        p3=professor_birthday[6:10]
        professor_password=p1+p2+p3
        professor_role = Role(name='Professor')
        professor_ui = generateuniqueid("Professor")
        professor_type = "Professor"
        professor = Professor(uniqueid=professor_ui, name=professor_name, gender=professor_gender,
            department=professor_department, email=professor_email,
            birthday=professor_birthday, phone=professor_phone, active=True, type=professor_type)
        professor.password = password_manager.hash_password(professor_password)
        professor.roles = [professor_role,]
        db.session.add(professor)
        db.session.commit()
        return redirect(url_for('professor_roster'))
    return render_template('create_professor.html', form = form)

@app.route('/create_administrator', methods=['GET', 'POST'])
# @login_required
# @roles_required('Admin')
def create_administrator():
    # Get information from the form.
    form = CreateAdministratorForm()
    # Get information from the form.
    if form.validate_on_submit():
        admin_name = form.admin_name.data
        admin_gender = form.admin_gender.data
        admin_department = form.admin_department.data
        admin_email = form.admin_email.data
        t = form.admin_birthday.data
        admin_birthday = t.strftime('%m/%d/%Y')
        admin_phone = str(form.admin_phone.data)
        a1=admin_birthday[:2]
        a2=admin_birthday[3:5]
        a3=admin_birthday[6:10]
        admin_password=a1+a2+a3
        admin_role = Role(name='Admin')
        admin_ui = generateuniqueid("Administrator")
        admin_type = "Administrator"
        admin = Administrator(uniqueid=admin_ui, name=admin_name, gender=admin_gender,
            department=admin_department, email=admin_email,
            birthday=admin_birthday, phone=admin_phone, active=True, type=admin_type)
        admin.password = password_manager.hash_password(admin_password)
        admin.roles = [admin_role,]
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('administrator_roster'))
    return render_template('create_administrator.html', form = form)

@app.route('/delete/<type>/<int:id>')
@login_required
@roles_required('Admin')
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
@login_required
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
@login_required
def details(type, id):
    if type == "Student":
        student = Student.query.get(id)
        return render_template('students_details.html', student=student)
    elif type == "Professor":
        prof = Professor.query.get(id)
        return render_template('professor_details.html', prof=prof)
    elif type == "Administrator":
        admin = Administrator.query.get(id)
        return render_template('administrator_details.html', admin=admin)
    elif type == "Course":
        course = Course.query.get(id)
        professor = Professor.query.get(course.professor_id)
        assignments = course.assignments
        return render_template('course_details.html', course=course, professor=professor, assignments=assignments)
    else:
        return render_template('error.html')

#Creates Courses
@app.route('/create_course', methods=['GET', 'POST'])
@login_required
@roles_required('Admin')
def create_course():
    # Get information from the form.
    professors = Professor.query.all()
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        course_subject = request.form.get('course_subject')
        course_number = request.form.get('course_number')
        professor_name = request.form.get('professor_name')
        day = request.form.get('days')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        professor = Professor.query.filter_by(name=professor_name).first()
        professor_id = professor.id
        course_ui = generateuniqueid("Course")
        course = Course(uniqueid=course_ui, name=course_name, subject=course_subject, number=course_number, professor_id=professor_id, day=day, start_time=start_time, end_time=end_time)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('course_list'))
    return render_template('create_course.html', professors=professors)

@app.route('/course_list')
@login_required
@roles_required('Admin')
def course_list():
    courses = Course.query.all()
    return render_template('course_list.html', courses=courses)

@app.route('/change_password/<type>/<int:id>',methods=['GET','POST'])
@login_required
def change_password(type, id):
    if type == "Student":
        user = Student.query.get(id)
        # if user.is_authenticated:
        #     return redirect(url_for('index', type="Student", id=id))
        form = PasswordForm()
        if form.validate_on_submit():
            if user is None or not password_manager.verify_password(form.password.data, user.password):
                    flash('Invalid password')
                    return redirect(url_for('change_password', type='Student', id=id))
            user.password = password_manager.hash_password(form.np.data)
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
            if user is None or not password_manager.verify_password(form.password.data, user.password):
                    flash('Invalid password')
                    return redirect(url_for('change_password', type='Professor', id=id))
            user.password = password_manager.hash_password(form.np.data)
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
            if user is None or not password_manager.verify_password(form.password.data, user.password):
                    flash('Invalid password')
                    return redirect(url_for('change_password', type='Administrator', id=id))
            user.password = password_manager.hash_password(form.np.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index', type='Administrator', id=id))
        return render_template('admin_password.html', form=form)
    else:
        return render_template('error.html')

@app.route('/registered/<int:id>')
@login_required
# @roles_required('Student')
def registered(id):
    student = Student.query.get(id)
    registered = student.courses
    return render_template('registered.html', student=student, registered=registered)

@app.route('/search_course/<int:id>', methods=['GET','POST'])
@login_required
# @roles_required('Student')
def search_course(id):
    form = SearchCourseForm()
    #course_subject = form.course_subject.data
    course_name = form.course_name.data
    #course_number = form.course_number.data
    #professor_id = form.professor_id.data
    courses = Course.query.filter(Course.name==course_name)
    #(Course.subject == course_subject) if course_subject != None else None, (Course.name==course_name) if course_name != None else None, (Course.number == course_number) if course_number != None else None, (Course.professor_id==professor_id) if professor_id != None else None
    #print(course_name)
    professor=Professor
    #if course_subject != None else None, Course.name.like('%' + course_name + '%') if course_name != None else None, Course.number.like('%' + course_number + '%') if course_number != None else None, Course.professor_id.like('%' + professor_id + '%') if professor_id != None else None)
    #Professor.query.filter(Professor.professor_name)
    return render_template('search_course.html', form=form, Professor=professor, courses=courses)

@app.route('/register/<int:id>', methods=['GET','POST'])
@login_required
@roles_required('Student')
def register(id):
    form = RegisterCourseForm()
    if form.validate_on_submit():
        course_subject=form.course_subject.data
        return redirect(url_for('results', id=id, subject=course_subject))
    return render_template('register.html', form=form)

@app.route('/results/<int:id>/<subject>')
def results(id, subject):
    student = Student.query.get(id)
    courses = Course.query.filter_by(subject=subject).all()
    return render_template('results.html', student=student, courses=courses)

@app.route('/course_overview/<int:id>/<int:course_id>', methods=['GET','POST'])
def course_overview(id, course_id):
    course = Course.query.get(course_id)
    student = Student.query.get(id)
    professor = Professor.query.get(course.professor_id)
    scraper = RateMyProfScraper(842)
    json_object = scraper.SearchProfessor(professor.name)
    tDept = scraper.PrintProfessorDetail('tDept')
    tSid = scraper.PrintProfessorDetail('tSid')
    institution_name = scraper.PrintProfessorDetail('institution_name')
    tid = scraper.PrintProfessorDetail('tid')
    tNumRatings = scraper.PrintProfessorDetail('tNumRatings')
    rating_class = scraper.PrintProfessorDetail('rating_class')
    overall_rating=scraper.PrintProfessorDetail("overall_rating")
    url = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=' + str(tid)
    if request.method == 'POST':
        student.courses.append(course)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('registered', id=id))
    return render_template('course_overview.html', tDept=tDept, tSid=tSid, institution_name=institution_name,
                tid=tid, tNumRatings=tNumRatings, rating_class=rating_class, overall_rating=overall_rating,
                student=student, course=course, professor=professor, url=url)

@app.route('/add_assignment/<int:id>', methods=['GET','POST'])
@login_required
@roles_required('Professor')
def add_assignment(id):
    form = CreateAssignment()
    course = Course.query.get(id)
    students = course.students
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        type = form.type.data
        total = form.total.data
        assignment = Assignment(name=name, description=description, type=type, total=total, course_id=id)
        db.session.add(assignment)
        db.session.commit()
        for student in students:
            submission = Submission(student_id=student.id, assign_id=assignment.id, assign_total=assignment.total, assign_course_id=assignment.course_id)
            db.session.add(submission)
            db.session.commit()
        return redirect(url_for('details', type='Course',  id=id))
    return render_template('add_assignment.html', form=form)

@app.route('/assignment/<int:id>/')
@login_required
# @roles_required('Student', 'Professor')
def assignment(id):
    assignment = Assignment.query.get(id)
    return render_template('assignment.html', assignment=assignment)

@app.route('/course/roster/<int:id>')
@login_required
# @roles_required('Student', 'Professor')
def student_course_roster(id):
    course = Course.query.get(id)
    students = course.students
    return render_template('course_roster.html', course=course, students=students)

@app.route('/student_grades/<int:id>/<int:course_id>')
@login_required
# @roles_required('Student', 'Professor')	# @roles_required('Student', 'Professor')
def student_grades(id, course_id):
    course = Course.query.get(course_id)
    submissions = Submission.query.filter_by(student_id=id, assign_course_id=course_id).all()
    student = Student.query.get(id)
    total_earned = 0
    total_points = 0
    letter_grade = ""
    for submission in submissions:
        total_earned += submission.points
        total_points += submission.assign_total
    percentage = (total_earned/total_points)*100
    if percentage >= 95.0:
        letter_grade = "A+"
    elif percentage < 95.0 and percentage >= 91.0:
        letter_grade = "A"
    elif percentage < 91.0 and percentage >= 87.0:
        letter_grade = "B+"
    elif percentage < 87.0 and percentage >= 83.0:
        letter_grade = "B"
    elif percentage < 83.0 and percentage >= 80.0:
        letter_grade = "B-"
    elif percentage < 80.0 and percentage >= 77.0:
        letter_grade = "C+"
    elif percentage < 77.0 and percentage >= 74.0:
        letter_grade = "C"
    elif percentage < 74.0 and percentage >= 70.0:
        letter_grade = "C-"
    elif percentage < 70.0 and percentage >= 67.0:
        letter_grade = "D+"
    elif percentage < 67.0 and percentage >= 65.0:
        letter_grade = "D"
    elif percentage < 65.0 and percentage >= 60.0:
        letter_grade = "D-"
    else :
        letter_grade = "F"
    return render_template('student_grades.html', course=course, submissions=submissions, student=student,
                            total_earned=total_earned, total_points=total_points, percentage=percentage, letter_grade=letter_grade)

@app.route('/classes/grades/<int:id>')
@login_required
def student_class_gradebook(id):
    student = Student.query.get(id)
    courses = student.courses
    return render_template('classes_gradebook.html', courses=courses, student=student)

@app.route('/course_roster/<int:id>/<int:course_id>')
@login_required
@roles_required('Student', 'Professor')
def course_roster(id,course_id):
    submissions = Submission.query.filter_by(student_id=id, assign_course_id=course_id)
    student = Student.query.get(id)
    return render_template('student_grades.html', submissions=submissions, student=student)

@app.route('/submission_page/<int:id>/<int:assignment_id>', methods=['GET','POST'])
@login_required
@roles_required('Student')
def submission_page(id, assignment_id):
    assignment = Assignment.query.get(assignment_id)
    student = Student.query.get(id)
    if request.method == 'POST' and 'file' in request.files:
        filename = files.save(request.files['file'])
        submission = Submission.query.filter_by(student_id=id, assign_course_id=assignment.course_id).first()
        submission.set_file(filename)
        submission.submitted(True)
        db.session.add(submission)
        db.session.commit()
        return redirect(url_for('submission_confirmation',  id=submission.id))
    return render_template('submission_page.html', student=student, assignment=assignment)

@app.route('/submission_confirmation/<int:id>')
@login_required
@roles_required('Student')
def submission_confirmation(id):
    submission = Submission.query.get(id)
    student = Student.query.get(submission.student_id)
    return render_template('submission_confirmation.html', submission=submission, student=student)

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
@app.route('/gpa/<int:id>', methods=['GET', 'POST'])
def gpa(id):
    student = Student.query.get(id)
    courses = student.courses
    grade = ""
    counter = 0
    counter2 = 0
    for course in courses:
        counter += 1
    for course in courses:
        total_earned = 0
        total_points = 0
        letter_grade = ""
        counter2 += 1
        submissions = Submission.query.filter_by(student_id=id, assign_course_id=course.id).all()
        for submission in submissions:
            total_earned += submission.points
            total_points += submission.assign_total
        percentage = (total_earned/total_points)*100
        if percentage >= 95.0:
            letter_grade = "A+"
        elif percentage < 95.0 and percentage >= 91.0:
            letter_grade = "A"
        elif percentage < 91.0 and percentage >= 87.0:
            letter_grade = "B+"
        elif percentage < 87.0 and percentage >= 83.0:
            letter_grade = "B"
        elif percentage < 83.0 and percentage >= 80.0:
            letter_grade = "B-"
        elif percentage < 80.0 and percentage >= 77.0:
            letter_grade = "C+"
        elif percentage < 77.0 and percentage >= 74.0:
            letter_grade = "C"
        elif percentage < 74.0 and percentage >= 70.0:
            letter_grade = "C-"
        elif percentage < 70.0 and percentage >= 67.0:
            letter_grade = "D+"
        elif percentage < 67.0 and percentage >= 65.0:
            letter_grade = "D"
        elif percentage < 65.0 and percentage >= 60.0:
            letter_grade = "D-"
        else :
            letter_grade = "F"
        if counter2 < counter:
            grade += letter_grade+", "
        else:
            grade += letter_grade

    result=0
    result1=0
    form = GPAPForm()
    GPA_chart = pygal.Bar()
    GPA_chart2 = pygal.Radar()
    graph_data = GPA_chart.render_data_uri()
    graph_data2 = GPA_chart2.render_data_uri()
    result = gpa_calculater(grade)
    current_GPA = result
    Num_of_course = counter
    if result != 0:
        grades = a_4(grade)
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
    if form.validate_on_submit():
        future_grades = form.future_grades.data
        # = request.form.get('student_gender')
        result1 = gpa_predictor(current_GPA, Num_of_course, future_grades)

    return render_template('gpa.html', graph_data = graph_data, graph_data2 = graph_data2, result = result, form = form, result1 =result1, grade=grade, current_GPA=current_GPA, counter=counter, student=student)

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

def ratemyprof():
    scrape = RateMyProfScraper(842)
    return scrape

def generateuniqueid(type):
    if type == "Administrator":  #Prefix:1
        ui = Unique.query.get(1)
        id_prefix = str(ui.prefix)
        id_count = str(ui.count)
        unique_id = id_prefix+id_count
        ui.count = ui.count+1
    elif type == "Professor":  #Prefix:2,3,4
        ui = Unique.query.get(2)
        id_prefix = str(ui.prefix)
        id_count = str(ui.count)
        unique_id = id_prefix+id_count
        ui.count = ui.count+1
    elif type == "Student": #Prefix:5,6,7
        ui = Unique.query.get(5)
        id_prefix = str(ui.prefix)
        id_count = str(ui.count)
        unique_id = id_prefix+id_count
        ui.count = ui.count+1
    elif type == "Course": #Prefix:8,9
        ui = Unique.query.get(8)
        id_prefix = str(ui.prefix)
        id_count = str(ui.count)
        unique_id = id_prefix+id_count
        ui.count = ui.count+1
    else:
        unique_id = null
    return unique_id
