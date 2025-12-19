from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField

class PostMessageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": 'Enter your name...'})
    body = TextAreaField('Message', validators=[DataRequired()], render_kw={"placeholder": 'Enter a message...'})
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(5,20, message="Username must be between 3 and 20 characters")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, message="Password must be at least 3 characters long.")])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Password confirmation is required."), 
        EqualTo('password', message="Passwords must match."),])
    submit = SubmitField('Signup')
    