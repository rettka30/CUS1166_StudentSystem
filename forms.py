from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, RadioField, DateField, FloatField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import Student, Professor, Administrator


class LoginForm(FlaskForm):
    id = IntegerField('ID Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    np = StringField('New Password', validators = [DataRequired()])
    submit = SubmitField('Change')

class GPAForm(FlaskForm):
    current_grades = StringField('Current Grades:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class GPAPForm(FlaskForm):
    current_GPA =  FloatField('Current GPA:', validators=[DataRequired()])
    Num_of_course = IntegerField('Num of Course took:', validators=[DataRequired()])
    future_grades = StringField('predict future Grades:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CreateStudentForm(FlaskForm):
    student_name = StringField('Student Name:', validators = [DataRequired()])
    student_gender = RadioField('Student Gender:', choices = [('Female','Female'),('Male','Male')])
    student_year = StringField('Year In School:', validators = [DataRequired()])
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
