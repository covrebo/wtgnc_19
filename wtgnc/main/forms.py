from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from wtgnc.main.utils import generate_week_num_list


# TODO: Get choices list from the schedule module - make list dynamic
class WeekSelectionForm(FlaskForm):
    # Form field to choose the week to display data from
    week = SelectField('Choose the week from the drop down list', validators=[
        DataRequired()
        ], coerce=str)
    submit = SubmitField('Set Week')