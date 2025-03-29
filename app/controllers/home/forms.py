from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
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

