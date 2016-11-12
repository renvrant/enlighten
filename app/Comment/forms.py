from flask_wtf import FlaskForm  #, RecaptchaField
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class CommentForm(FlaskForm):
    title = TextField('Comment Title', validators=[Length(min=5)])
    body = TextAreaField('Comment Body', validators=[DataRequired(), Length(min=5, max=255)])
