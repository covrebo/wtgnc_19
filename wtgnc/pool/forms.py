from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired


# Form to submit picks each week
class PickSelectionForm(FlaskForm):
    # Form field to choose the week to display data from
    pick_1 = SelectField(validators=[
        DataRequired()
        ], coerce=str)
    pick_2 = SelectField(validators=[
        DataRequired()
        ], coerce=str)
    pick_3 = SelectField(validators=[
        DataRequired()
        ], coerce=str)
    pick_4 = SelectField(validators=[
        DataRequired()
        ], coerce=str)
    make = SelectField(validators=[
        DataRequired()
        ], coerce=str)
    submit = SubmitField('Set Roster')


# Form to enter a weekly pool result
class WeeklyResultForm(FlaskForm):
    # Form field to choose the week to display data from
    user = SelectField(validators=[
        DataRequired()
    ], coerce=str)
    points = IntegerField('Points', validators=[
        DataRequired()
    ])
    rank = IntegerField('Rank', validators=[
        DataRequired()
    ])
    submit = SubmitField('Submit Result')


# Form to update a weekly pool result
class WeeklyResultUpdateForm(FlaskForm):
    # Form field to choose the week to display data from
    points = IntegerField('Points', validators=[
        DataRequired()
    ])
    rank = IntegerField('Rank', validators=[
        DataRequired()
    ])
    submit = SubmitField('Update Result')


# Form to enter a weekly pool standing
class WeeklyStandingForm(FlaskForm):
    # Form field to choose the week to display data from
    user = SelectField(validators=[
        DataRequired()
    ], coerce=str)
    points = IntegerField('Points', validators=[
        DataRequired()
    ])
    rank = IntegerField('Rank', validators=[
        DataRequired()
    ])
    wins = IntegerField('Wins')
    submit = SubmitField('Submit Standing')


# Form to update a weekly pool standing
class WeeklyStandingUpdateForm(FlaskForm):
    # Form field to choose the week to display data from
    points = IntegerField('Points', validators=[
        DataRequired()
    ])
    rank = IntegerField('Rank', validators=[
        DataRequired()
    ])
    wins = IntegerField('Wins')
    submit = SubmitField('Submit Standing')
