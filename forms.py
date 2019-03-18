from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import Student, Professor, Administrator


class LoginForm(FlaskForm):
    id = IntegerField('ID Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class GPAForm(FlaskForm):
    current_grades = StringField('Current Grades', validators=[DataRequired()])
    submit = SubmitField('Submit')
