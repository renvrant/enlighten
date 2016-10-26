from flask_wtf import FlaskForm
from wtforms import TextAreaField, TextField
from wtforms.validators import DataRequired


class CreateTransgressionForm(FlaskForm):

    title = TextField('Title', validators=[DataRequired('A title is required')])
    content = TextAreaField('Content', validators=[DataRequired('Please add some contnet')])
