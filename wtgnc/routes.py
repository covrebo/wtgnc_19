from flask_login import login_user, current_user, logout_user, login_required
from wtgnc import app, db
from flask import render_template, url_for, session, flash, redirect, request
from wtgnc.forms import WeekSelectionForm, RegistrationForm, LoginForm, PickSelectionForm, EntryForm, EventForm
from wtgnc.models import User, Driver, Event, Pick

# TEMP import of entry list from another file
from wtgnc.data_vars import picks, entry_list_brief, pick_list


@app.route('/')
@app.route('/home')
def home():
    # TODO: List the standings on the home page
    week = Event.query.filter_by(week_id=1).first()
    return render_template('home.html', entry_list=entry_list_brief, week=week, pick_list=pick_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated and current_user.role != 'admin':
        flash('You are already logged in as a registered user.  Contact a commissioner to register a new account.', 'info')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_first_name=form.user_first_name.data, user_last_name=form.user_last_name.data, display_name=form.display_name.data, email=form.email.data)
        user.set_pw(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.display_name.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # TODO: Does this protect against SQL injection?
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"{current_user.display_name} successfully logged in.", 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    if session.get('week_num') != None:
        session.pop('week_num')
    if session.get('week_name') != None:
        session.pop('week_name')
    flash('You have been logged out.')
    return redirect(url_for('home'))


# Route to the administration page
@app.route('/admin')
@login_required
# TODO: require user role of admin to view
def admin():
    return render_template('admin.html', title='Pool Admin')


# Route to the user account page
@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


# Route to submit weekly driver roster
@app.route('/pick-page', methods=['GET', 'POST'])
@login_required
def pick_page():
    # TODO add login requirement
    # TODO add modal to the page to confirm which week they are pick for
    form = PickSelectionForm()
    if form.validate_on_submit():
        picks = Pick(week=session['week_num'], display_name=current_user.display_name, driver_1=form.pick_1.data,
                     driver_2=form.pick_2.data, driver_3=form.pick_3.data, driver_4=form.pick_4.data,
                     make=form.make.data, user_id=current_user.id)
        db.session.add(picks)
        db.session.commit()
        flash(f"You have submitted picks for {session['week_name']}.  Good Luck!", 'success')
        # TODO change redirect to pick summary page
        return redirect(url_for('picks_summary'))
    return render_template('pick-page.html', title='Pick Page', form=form)

@app.route('/picks-summary')
@login_required
# TODO: Allow users to update their picks if they are the ones that submitted them
def picks_summary():
    return render_template('picks.html', title='Pick Summary', picks=picks)

# Route to a set the session cookie to display the correct week
@app.route('/site-selection', methods=['GET', 'POST'])
@login_required
def week_selection():
    # Create a form to set the site value for the session
    form = WeekSelectionForm()
    if form.validate_on_submit():
        # Update week value in session cookie
        # TODO: Reorder query to retrieve the latest result https://stackoverflow.com/questions/8551952/how-to-get-last-record
        week = Event.query.filter_by(week_id=form.week.data).first()
        session['week_num'] = week.week_id
        session['week_name'] = week.week_str
        flash(f"You are now looking at picks and results from {str(session['week_name'])}.", 'success')
        return redirect(url_for('home'))
    return render_template('week-selection.html', title='Week Selection', form=form)


# Route to create a driver entry
@app.route('/driver-entry', methods=['GET', 'POST'])
@login_required
def driver_entry():
    form = EntryForm()
    if form.validate_on_submit():
        driver = Driver(car_number=form.car_number.data, driver=form.driver.data, sponsor=form.sponsor.data, make=form.make.data, team=form.team.data)
        db.session.add(driver)
        db.session.commit()
        flash(f"You have added {form.driver.data}.", 'success')
        # TODO change redirect to pick summary page
        return redirect(url_for('home'))
    return render_template('driver-entry.html', title='Driver Entry', legend='Create Driver', form=form)


# Route to create a race entry
@app.route('/race-event', methods=['GET', 'POST'])
@login_required
def race_event():
    # TODO add login requirement
    # TODO: Style the date selection field properly
    form = EventForm()
    if form.validate_on_submit():
        event = Event(week_id=form.week.data, week_str=f"Week {form.week.data} - {form.track.data}", track=form.track.data, race=form.race.data, date=form.date.data)
        db.session.add(event)
        db.session.commit()
        flash(f"You have added the {form.race.data}.", 'success')
        # TODO change redirect to pick summary page
        return redirect(url_for('home'))
    return render_template('race-event.html', title='Race Event', legend='Create Race Event', form=form)

# TODO add and admin page with links to register new users, enter schedule event, enter a driver entry, update a driver entry, enter results, enter/update weekly results, enter/update standings.
# TODO add a route to submit races to the schedule