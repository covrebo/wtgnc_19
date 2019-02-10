from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtgnc.models import User
from wtgnc.data_vars import schedule_week_name, make_list, entry_list_brief

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
    password = PasswordField('Password', validators=[
        DataRequired()
        ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
        ])
    submit = SubmitField('Register')

    # Function to validate the unique username before submitting the form
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose another.')

    # Function to validate the unique username before submitting the form
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose another.')

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
        ], choices=schedule_week_name)
    submit = SubmitField('Set Week')

# Custom validator to make sure picks are unique
# TODO: Move this validation to the route in routes.py
# def pick_check_1(form, field):
#     if pick_1.data == pick_2.data or pick_1.data == pick_3.data:
#         raise ValidationError('Please pick three DIFFERENT drivers.')
#
# def pick_check_2(form, field):
#     if pick_2.data == pick_1.data or pick_2.data == pick_3.data:
#         raise ValidationError('Please pick three DIFFERENT drivers.')
#
# def pick_check_3(form, field):
#     if pick_3.data == pick_2.data or pick_3.data == pick_2.data:
#         raise ValidationError('Please pick three DIFFERENT drivers.')

# Form to submit picks each week
class PickSelectionForm(FlaskForm):
    # Form field to choose the week to display data from
    pick_1 = SelectField('Choose a driver from the drop down list', validators=[
        DataRequired()
        ], choices=entry_list_brief)
    pick_2 = SelectField('Choose a driver from the drop down list', validators=[
        DataRequired()
    ], choices=entry_list_brief)
    pick_3 = SelectField('Choose a driver from the drop down list', validators=[
        DataRequired()
        ], choices=entry_list_brief)
    make = SelectField('Choose a manufacturer from the drop down list', validators=[
        DataRequired()
        ], choices=make_list)
    submit = SubmitField('Set Roster')

# Form to create a driver entry
class EntryForm(FlaskForm):
    # Form field to choose the week to display data from
    car_number = IntegerField(validators=[
        DataRequired()
        ])
    driver = StringField('Driver Name', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    sponsor = StringField('Sponsor', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    make = SelectField(validators=[
        DataRequired()
        ], choices=make_list)
    team = StringField('Team', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    submit = SubmitField('Create Driver')

# Form to schedule a race event
class EventForm(FlaskForm):
    # Form field to choose the week to display data from
    week = IntegerField(validators=[
        DataRequired()
        ])
    track = StringField('Track', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    race = StringField('Race', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    date = DateField(format='%m-%d-%Y', validators=[
        DataRequired()
        ])
    submit = SubmitField('Create Event')

# TODO Form to enter weekly standings
# TODO Form to enter weekly results
# TODO Form to enter weekly NASCAR results
# TODO Form to enter weekly NASCAR standings