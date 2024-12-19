from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField

class PostMessageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": 'Enter your name...'})
    body = TextAreaField('Message', validators=[DataRequired()], render_kw={"placeholder": 'Enter a message...'})
    submit = SubmitField()