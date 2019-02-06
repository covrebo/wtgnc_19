import os
from flask import Flask, render_template, url_for, session, flash, redirect
from forms import WeekSelectionForm, RegistrationForm, LoginForm, PickSelectionForm

# TEMP import of entry list from another file
from data_vars import entry_list_detailed, picks

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/')
@app.route('/home')
def home():
    # TODO: List the standings on the home page
    return render_template('home.html', entry_list=entry_list_detailed)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.display_name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Route to submit weekly driver roster
@app.route('/pick-page', methods=['GET', 'POST'])
def pick_page():
    # TODO add login requirement
    # TODO add modal to the page to confirm which week they are pick for
    form = PickSelectionForm()
    if form.validate_on_submit():
        flash(f"You have set your roster for {str(session['week'])}.", 'success')
        # TODO change redirect to pick summary page
        return redirect(url_for('home'))
    return render_template('pick-page.html', title='Pick Page', form=form)

@app.route('/picks-summary')
# TODO add login requirement
# TODO: Allow users to update their picks if they are the ones that submitted them
def picks_summary():
    return render_template('picks.html', title='Pick Summary', picks=picks)

# Route to a set the session cookie to display the correct week
@app.route('/site-selection', methods=['GET', 'POST'])
# TODO add login requirement
def week_selection():
    # Create a form to set the site value for the session
    form = WeekSelectionForm()
    if form.validate_on_submit():
        # Update week value in session cookie
        session['week'] = form.week.data
        flash(f"You are now look at picks and results from {str(session['week'])}.", 'success')
        return redirect(url_for('home'))
    return render_template('week-selection.html', title='Week Selection', form=form)

if __name__ == '__main__':
    app.run()

# Feature requests
# TODO: Add pool rules to the about page
# TODO: Add pick history page
# TODO: Add race info pages such as entry list, starting lineup, and results
# TODO: Add active class to navigation links via http://jinja.pocoo.org/docs/tricks/
