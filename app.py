import os
from flask import Flask, render_template, url_for, session, flash, redirect
from forms import WeekSelectionForm, RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Example data
schedule = [
    {
        'week': 1,
        'track': 'Daytona',
        'date': (2019, 2, 17)
    },
    {
        'week': 2,
        'track': 'Atlanta',
        'date': (2019, 2, 24)
    },
    {
        'week': 3,
        'track': 'Las Vegas',
        'date': (2019, 3, 3)
    },
    {
        'week': 4,
        'track': 'Phoenix',
        'date': (2019, 3, 10)
    }
]

picks = [
    {
        'week': 1,
        'display_name': 'Chris O.',
        'pick_1': '#18 - Kyle Busch',
        'pick_2': '#48 - Jimmie Johnson',
        'pick_3': '#78 - Martin Truex Jr.',
        'manufacturer': 'Toyota'
    },
    {
        'week': 1,
        'display_name': 'Silver Fox',
        'pick_1': '#18 - Kyle Busch',
        'pick_2': '#48 - Jimmie Johnson',
        'pick_3': '#78 - Martin Truex Jr.',
        'manufacturer': 'Ford'
    },
    {
        'week': 1,
        'display_name': 'Ev-man',
        'pick_1': '#18 - Kyle Busch',
        'pick_2': '#48 - Jimmie Johnson',
        'pick_3': '#78 - Martin Truex Jr.',
        'manufacturer': 'Ford'
    },
    {
        'week': 2,
        'display_name': 'Jodi',
        'pick_1': '#18 - Kyle Busch',
        'pick_2': '#48 - Jimmie Johnson',
        'pick_3': '#78 - Martin Truex Jr.',
        'manufacturer': 'Chevy'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

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

@app.route('/picks-summary')
def picks_summary():
    return render_template('picks.html', title='Pick Summary', picks=picks)

# Route to a set the session cookie to display the correct week
@app.route('/site-selection', methods=['GET', 'POST'])
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
# TODO: Add active class to navigation links via http://jinja.pocoo.org/docs/tricks/
