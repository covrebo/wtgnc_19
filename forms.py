from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Create a registration form class
class RegistrationForm(FlaskForm):
    # Form fields with validators
    user_first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    user_last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    display_name = StringField('Display Name', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    email =  StringField('Email', validators=[
        DataRequired(),
        Email()
        ])
    password = PasswordField('Password', validators=[
        DataRequired()
        ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
        ])
    submit = SubmitField('Register')

    # # Function to validate the unique username before submitting the form
    # def validate_username(self, username):
    #     user = Users.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken, please choose another.')
    #
    # # Function to validate the unique username before submitting the form
    # def validate_email(self, email):
    #     user = Users.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken, please choose another.')

# Create a login form class
class LoginForm(FlaskForm):
    # Form fields with validators
    email =  StringField('Email', validators=[
        DataRequired(),
        Email()
        ])
    password = PasswordField('Password', validators=[
        DataRequired()
        ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class WeekSelectionForm(FlaskForm):
    # Form field to choose the week to display data from
    week = SelectField('Choose the week from the drop down list', validators=[
        DataRequired()
        ], choices=[('Week 1 - Daytona', 'Week 1 - Daytona'),
                    ('Week 2 - Atlanta', 'Week 2 - Atlanta'),
                    ('Week 3 - Las Vegas', 'Week 3 - Las Vegas'),
                    ('Week 4 - Phoenix', 'Week 4 - Phoenix'),
                    ('Week 4 - Phoenix', 'Week 4 - Phoenix'),
        ])
    submit = SubmitField('Set Week')