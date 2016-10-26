from flask_wtf import FlaskForm  #, RecaptchaField
from wtforms import TextField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):

    email = TextField('Email', validators=[
        DataRequired('Email is required'), Email('Please enter valid email')])
    password = PasswordField('Password', validators=[
        DataRequired('Password is Required')])


class CreateForm(FlaskForm):

    name = TextField('Username', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class EditForm(FlaskForm):

    title = TextField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    status = BooleanField('Approved')
