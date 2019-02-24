from flask import session
from wtgnc.models import User, Driver, Make


# function to create a dynamic entry list for the pick page that updates when new entries are added to the database
def generate_entry_list():
    # TODO: Return an error if a week has not been selected
    detailed_entry_list = Driver.query.filter_by(week=session['week_key']).order_by(Driver.car_number).all()
    entry_list = [('#' + str(driver.car_number) + ' - ' + driver.driver, '#' + str(driver.car_number) + ' - ' + driver.driver) for driver in detailed_entry_list]
    return entry_list


# TODO: Dynamically update by moving to routes file https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
def generate_make_list():
    # TODO: Return an error if a week has not been selected
    detailed_make_list = Make.query.all()
    make_list = [(make.make, make.make) for make in detailed_make_list]
    return make_list


# TODO: Dynamically update by moving to routes file https://stackoverflow.com/questions/46921823/dynamic-choices-wtforms-flask-selectfield
def generate_user_list():
    detailed_user_list = User.query.all()
    user_list = [(str(user.id), user.display_name) for user in detailed_user_list]
    return user_list


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
