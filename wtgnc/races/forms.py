from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length


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
        ], coerce=str)
    team = StringField('Team', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    active = BooleanField('Active', default='checked')
    submit = SubmitField('Submit')


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
    submit = SubmitField('Submit')


# Create a form to upload csv file
class UploadForm(FlaskForm):
    upload = FileField('Upload Entry List', validators=[
        FileAllowed(['csv'])
    ])
    submit = SubmitField('Upload File')


# Form to create a manufacturer
class MakeForm(FlaskForm):
    make = StringField('Make', validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    submit = SubmitField('Submit')