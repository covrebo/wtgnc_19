from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtgnc.models import User


# Create a registration form class
class RegistrationForm(FlaskForm):
    # Form fields with validators
    user_first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=20)
        ])
    user_last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=20)
        ])
    display_name = StringField('Display Name', validators=[
        DataRequired(),
        Length(min=2, max=30)
        ])
    email =  StringField('Email', validators=[
        DataRequired(),
        Email()
        ])
    role = SelectField('Role', validators=[
        DataRequired()
        ], choices=[
        ('user', 'User'),
        ('admin', 'Admin')
        ])
    password = PasswordField('Password', validators=[
        DataRequired()
        ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
        ])
    submit = SubmitField('Register')

    # Function to validate the unique username before submitting the form
    def validate_display_name(self, display_name):
        display_name = User.query.filter_by(display_name=display_name.data).first()
        if display_name:
            raise ValidationError('That display name is taken, please choose another.')

    # Function to validate the unique username before submitting the form
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose another.')


# Create a form to update account information
class UpdateAccountForm(FlaskForm):
    # Form fields with validators
    user_first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    user_last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    display_name = StringField('Display Name', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
        ])
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])
    ])
    submit = SubmitField('Update Account')

    # Function to validate the unique username before submitting the form
    def validate_display_name(self, display_name):
        if display_name.data != current_user.display_name:
            display_name = User.query.filter_by(display_name=display_name.data).first()
            if display_name:
                raise ValidationError('That display name is taken, please choose another.')

    # Function to validate the unique username before submitting the form
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please choose another.')


# Form to request a password reset
class RequestResetTokenForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Request Password Reset')

    # Function to validate the unique username before submitting the form
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('That account does not exist, contact a commissioner to register.')


# Form to reset a password
class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Set New Password')


# Create a login form class
class LoginForm(FlaskForm):
    # Form fields with validators
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
        ])
    password = PasswordField('Password', validators=[
        DataRequired()
        ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')