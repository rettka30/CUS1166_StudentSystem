from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SelectField, SubmitField, RadioField, DateField, FloatField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import Student, Professor, Administrator
from flask_user.forms import LoginForm

class LoginForm(LoginForm):
    id = IntegerField('ID Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    np = StringField('New Password', validators = [DataRequired()])
    submit = SubmitField('Change')

class RegisterCourseForm(FlaskForm):
    course_id = StringField('Course Subject:')
    submit = SubmitField('register')

class CreateAssignment(FlaskForm):
    name = StringField('Name of Assignment', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    total = IntegerField('Point Total for Assignment', validators=[DataRequired()])
    submit = SubmitField('Add Assignment')

class GPAForm(FlaskForm):
    current_grades = StringField('Current Grades:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class GPAPForm(FlaskForm):
    current_GPA =  FloatField('Current GPA:', validators=[DataRequired()])
    Num_of_course = IntegerField('Num of Course took:', validators=[DataRequired()])
    future_grades = StringField('predict future Grades:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchCourseForm(FlaskForm):
    #course_subject = StringField('Course Subject:')
    course_name = StringField('Course Name:')
    #course_number = StringField('Year In School:')
    #professor_id = IntegerField('Professor ID')
    submit = SubmitField('Submit')

class CreateStudentForm(FlaskForm):
    student_name = StringField('Student Name:', validators = [DataRequired()])
    student_gender = RadioField('Student Gender:', choices = [('Female','Female'),('Male','Male')])
    student_year = SelectField('Year In School:', choices=[('Freshman', 'Freshman'),
        ('Sophmore', 'Sophmore'), ('Junior', 'Junior'), ('Senior', 'Senior')], validators = [DataRequired()])
    student_email = EmailField('Email:', validators = [DataRequired(),Email()])
    student_birthday = DateField('Birthday: (ex. %m-%d-%y)', format='%m-%d-%Y')
    student_major = StringField('Major:', validators = [DataRequired()])
    student_phone = StringField('Phone Number:', validators = [DataRequired()])
    submit = SubmitField('Submit')

    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

class CreateProfessorForm(FlaskForm):
    professor_name = StringField('Professor Name:', validators = [DataRequired()])
    professor_gender = RadioField('Professor Gender:', choices = [('Female','Female'),('Male','Male')])
    professor_department = StringField('Department:', validators = [DataRequired()])
    professor_email = EmailField('Email:', validators = [DataRequired(),Email()])
    professor_birthday = DateField('Birthday: (ex. %m-%d-%y)', format='%m-%d-%Y')
    professor_phone = StringField('Phone Number:', validators = [DataRequired()])
    submit = SubmitField('Submit')

    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

class CreateAdministratorForm(FlaskForm):
    admin_name = StringField('Administrator Name:', validators = [DataRequired()])
    admin_gender = RadioField('Administrator Gender:', choices = [('Female','Female'),('Male','Male')])
    admin_department = StringField('Department:', validators = [DataRequired()])
    admin_email = EmailField('Email:', validators = [DataRequired(),Email()])
    admin_birthday = DateField('Birthday: (ex. %m-%d-%y)', format='%m-%d-%Y')
    admin_phone = StringField('Phone Number:', validators = [DataRequired()])
    submit = SubmitField('Submit')

    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
