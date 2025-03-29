from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class ProfileForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(),
        Length(min=2, max=20)
    ])


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', [
        DataRequired(),
        Length(min=8)
    ])
    new_password = PasswordField('New Password', [
        DataRequired(),
        Length(min=8),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm New Password')

class DiaryEntryForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=100, message="Title cannot exceed 100 characters")
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(message="Content cannot be empty")
    ])