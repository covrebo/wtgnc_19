from flask import render_template, url_for, session, flash, redirect, Blueprint
from wtgnc.main.forms import WeekSelectionForm
from wtgnc.main.utils import generate_week_num_list
from wtgnc.models import Event

main = Blueprint('main', __name__,template_folder='templates')


@main.route('/')
@main.route('/home')
def home():
    # TODO: List the standings on the home page
    return render_template('main/home.html', title='Home')


# Route to the about page
@main.route('/about')
def about():
    return render_template('main/about.html', title='About')


# Route to the privacy policy page
@main.route('/privacy-policy')
def privacy_policy():
    return render_template('main/privacy-policy.html', title='Privacy Policy')


# Route to a set the session variable to display the correct week
@main.route('/week-selection', methods=['GET', 'POST'])
def week_selection():
    # Create a form to set the site value for the session
    form = WeekSelectionForm()
    form.week.choices = generate_week_num_list()
    if form.validate_on_submit():
        # Update week value in session cookie
        # TODO: Reorder query to retrieve the latest result https://stackoverflow.com/questions/8551952/how-to-get-last-record
        week = Event.query.filter_by(week_id=form.week.data).first()
        session['week_num'] = week.week_id
        session['week_name'] = week.week_str
        session['week_key'] = week.id
        flash(f"You are now looking at picks and results from {str(session['week_name'])}.", 'success')
        return redirect(url_for('main.home'))
    return render_template('main/week-selection.html', title='Week Selection', form=form)