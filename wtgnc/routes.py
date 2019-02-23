import os
import secrets
import csv
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required
from wtgnc import app, db
from flask import render_template, url_for, session, flash, redirect, request, abort
from werkzeug.utils import secure_filename
from wtgnc.forms import WeekSelectionForm, RegistrationForm, LoginForm, PickSelectionForm, EntryForm, EventForm, WeeklyResultForm, WeeklyStandingForm, UpdateAccountForm, WeeklyResultUpdateForm, WeeklyStandingUpdateForm, UploadForm
from wtgnc.models import User, Driver, Event, Pick, WeeklyResult, WeeklyStanding, Result, StartingLineup


@app.route('/')
@app.route('/home')
def home():
    # TODO: List the standings on the home page
    return render_template('home.html', title='Home')


# Route to the about page
@app.route('/about')
def about():
    return render_template('about.html', title='About')


# Route to the privacy policy page
@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html', title='Privacy Policy')


@app.route('/register', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('home'))
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


# Function to rename and save profile pictures
def save_picture(form_picture):
    # Rename file with random name to avoid filename collisions
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # Resize the image to 125x125 pixels
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # Save the picture with a new name and return the filename so it can be updated in the database
    i.save(picture_path)
    return picture_fn


# Route to the user account page
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # TODO: Add a weekly pick, result, and standings summary for each account
    # TODO: Add driver popularity and other stats to account summary
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_image = picture_file
            # TODO: delete old pictures from the file system
        current_user.user_first_name = form.user_first_name.data
        current_user.user_last_name = form.user_last_name.data
        current_user.display_name = form.display_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"Account information updated for {current_user.display_name}", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.user_first_name.data = current_user.user_first_name
        form.user_last_name.data = current_user.user_last_name
        form.display_name.data = current_user.display_name
        form.email.data = current_user.email
    image_file = url_for('static', filename=f"profile_pics/{current_user.profile_image}")
    # TODO: Add link to update weekly picks
    # TODO: Add statistics to account - driver popularity, weekly avg points, wins, etc.
    picks = Pick.query.filter_by(user_id=current_user.id).order_by(Pick.week).all()
    results = WeeklyResult.query.filter_by(user_id=current_user.id).order_by(WeeklyResult.week).all()
    standings = WeeklyStanding.query.filter_by(user_id=current_user.id).order_by(WeeklyStanding.week).all()
    return render_template('account.html', title='Account', legend='Account Info', image_file=image_file, form=form, picks=picks, results=results, standings=standings)


# function to create a dynamic entry list for the pick page that updates when new entries are added to the database
def generate_entry_list():
    # TODO: Return an error if a week has not been selected
    detailed_entry_list = Driver.query.filter_by(week=session['week_key']).order_by(Driver.car_number).all()
    entry_list = [('#' + str(driver.car_number) + ' - ' + driver.driver, '#' + str(driver.car_number) + ' - ' + driver.driver) for driver in detailed_entry_list]
    return entry_list

# Route to submit weekly driver roster
@app.route('/pick-page', methods=['GET', 'POST'])
@login_required
def pick_page():
    # TODO add modal to the page to confirm which week they are pick for
    form = PickSelectionForm()
    form.pick_1.choices = generate_entry_list()
    form.pick_2.choices = generate_entry_list()
    form.pick_3.choices = generate_entry_list()
    form.pick_4.choices = generate_entry_list()
    if form.validate_on_submit():
        pick_check = Pick.query.filter_by(week=session['week_num'], user_id=current_user.id).first()
        if pick_check:
            flash(f"Sorry, you have already submitted picks for {session['week_name']}.  Please visit the account page to update your picks or select a different week.", 'info')
            redirect(url_for('pick_page'))
        else:
            picks = Pick(week=session['week_num'], display_name=current_user.display_name, driver_1=form.pick_1.data,
                         driver_2=form.pick_2.data, driver_3=form.pick_3.data, driver_4=form.pick_4.data,
                         make=form.make.data, user_id=current_user.id)
            db.session.add(picks)
            db.session.commit()
            flash(f"You have submitted picks for {session['week_name']}.  Good Luck!", 'success')
            return redirect(url_for('picks_summary'))
    return render_template('pick-page.html', title='Pick Page', form=form)


# Route to display the weekly picks
@app.route('/picks-summary')
@login_required
# TODO: Allow users to update their picks if they are the ones that submitted them
def picks_summary():
    picks = Pick.query.filter_by(week=session['week_num']).all()
    return render_template('picks.html', title='Pick Summary', picks=picks)


# Route to a set the session variable to display the correct week
@app.route('/week-selection', methods=['GET', 'POST'])
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
        session['week_key'] = week.id
        flash(f"You are now looking at picks and results from {str(session['week_name'])}.", 'success')
        return redirect(url_for('home'))
    return render_template('week-selection.html', title='Week Selection', form=form)


# Route to the administration page
@app.route('/admin')
@login_required
def admin():
    if current_user.role == 'admin':
        return render_template('admin.html', title='Pool Admin')
    else:
        flash('You must be a commissioner to view the admin page!', 'warning')
        return redirect(url_for('home'))


# Route to show the current list of pool members
@app.route('/member-list')
def member_list():
    user_list = User.query.order_by(User.user_last_name).all()
    return render_template('members.html', title='Member List', user_list=user_list)


# Route to upload an entry list csv
@app.route('/upload-entry-list', methods=['GET', 'POST'])
@login_required
def entry_list_upload():
    form = UploadForm()
    # Upload the file to uploads folder
    if form.validate_on_submit():
        if form.upload.data:
            file = form.upload.data
            f_name = secure_filename(file.filename)
            f_path = os.path.join(app.root_path, 'static/uploads', f_name)
            file.save(f_path)
            file = open(f_path, "r", encoding="utf-8")
            csv_reader = csv.reader(file, delimiter=',')
            # Skip the headers
            next(csv_reader)
            for row in csv_reader:
                # TODO: Add check for correct data in each field
                entry = Driver(week=int(session['week_key']), car_number=int(row[0]), driver=row[1], sponsor=row[2], make=row[3], team=row[4])
                db.session.add(entry)
                db.session.commit()
            # Delete the file
            if os.path.exists(f_path):
                os.remove(f_path)
            flash('You have successfully uploaded the entry list', 'success')
            return redirect(url_for('entry_list'))
    else:
        return render_template('upload-file.html', title='Upload Entry List', legend='Upload Entry List', form=form)


# Route to create a driver entry
@app.route('/driver-entry', methods=['GET', 'POST'])
@login_required
def driver_entry():
    form = EntryForm()
    if form.validate_on_submit():
        driver = Driver(week=int(session['week_num']), car_number=form.car_number.data, driver=form.driver.data, sponsor=form.sponsor.data, make=form.make.data, team=form.team.data)
        db.session.add(driver)
        db.session.commit()
        flash(f"You have added {form.driver.data}.", 'success')
        return redirect(url_for('entry_list'))
    return render_template('driver-entry.html', title='Driver Entry', legend='Create Driver', form=form)


# Route to view a driver entry
@app.route('/driver/<int:driver_id>', methods=['GET', 'POST'])
@login_required
def driver(driver_id):
    # TODO: Add a performance summary for each race to the driver page
    # TODO: Add an popularity measure, average start, average finish, average stage points, and average total points stat to each driver.
    driver = Driver.query.get_or_404(driver_id)
    return render_template('driver.html', title='Driver Summary', driver=driver)


# Route to update a driver entry
@app.route('/driver/<int:driver_id>/update', methods=['GET', 'POST'])
@login_required
def update_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    if current_user.role != 'admin':
        abort(403)
    form = EntryForm()
    if form.validate_on_submit():
        driver.car_number = form.car_number.data
        driver.driver = form.driver.data
        driver.sponsor = form.sponsor.data
        driver.make = form.make.data
        driver.team = form.team.data
        driver.active = form.active.data
        db.session.commit()
        flash(f"Driver information updated for {form.driver.data}", 'success')
        return redirect(url_for('entry_list'))
    elif request.method == 'GET':
        form.car_number.data = driver.car_number
        form.driver.data = driver.driver
        form.sponsor.data = driver.sponsor
        form.make.data = driver.make
        form.team.data = driver.team
        form.active.data = driver.active
    return render_template('driver-entry.html', title='Driver Update', legend='Update Driver', form=form)


# Route to delete a driver entry
@app.route('/driver/<int:driver_id>/delete', methods=['POST'])
@login_required
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(driver)
    db.session.commit()
    flash(f"Driver has been deleted", 'success')
    return redirect(url_for('entry_list'))


# Route to show the current entry list
@app.route('/entry-list')
def entry_list():
    entry_list = Driver.query.order_by(Driver.car_number).all()
    return render_template('entry-list.html', title='Entry List', entry_list=entry_list)


# Route to create a race entry
@app.route('/race-event', methods=['GET', 'POST'])
@login_required
def race_event():
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


# Route to view a race entry
@app.route('/race/<int:race_id>', methods=['GET', 'POST'])
@login_required
def race(race_id):
    race = Event.query.get_or_404(race_id)
    return render_template('race.html', title='Race Summary', race=race)


# Route to update a race entry
@app.route('/race/<int:race_id>/update', methods=['GET', 'POST'])
@login_required
def update_race(race_id):
    race = Event.query.get_or_404(race_id)
    if current_user.role != 'admin':
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        race.week_id = form.week.data
        race.week_str = f"Week {form.week.data} - {form.track.data}"
        race.track = form.track.data
        race.race = form.race.data
        race.date = form.date.data
        db.session.commit()
        flash(f"Race information updated for the {form.race.data}", 'success')
        return redirect(url_for('schedule'))
    elif request.method == 'GET':
        form.week.data = race.week_id
        form.track.data = race.track
        form.race.data = race.race
        form.date.data = race.date
    return render_template('race-event.html', title='Race Update', legend='Update Race', form=form)


# Route to delete a race entry
@app.route('/race/<int:race_id>/delete', methods=['POST'])
@login_required
def delete_race(race_id):
    race = Event.query.get_or_404(race_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(race)
    db.session.commit()
    flash(f"Race has been deleted", 'success')
    return redirect(url_for('schedule'))


# Route to show the current schedule
@app.route('/schedule')
def schedule():
    schedule = Event.query.all()
    return render_template('schedule.html', title='Schedule', schedule=schedule)


# Route to create a weekly result
@app.route('/weekly-result-entry', methods=['GET', 'POST'])
@login_required
def weekly_result_entry():
    form = WeeklyResultForm()
    if form.validate_on_submit():
        weekly_result = WeeklyResult(week=int(session['week_num']), user_id=int(form.user.data), rank=form.rank.data, points=form.points.data)
        db.session.add(weekly_result)
        db.session.commit()
        flash("You have added a weekly result.", 'success')
        return redirect(url_for('weekly_results'))
    return render_template('weekly-result-entry.html', title='Weekly Result Entry', legend='Create Result', form=form)


# Route to view a weekly result
@app.route('/weekly-result/<int:weekly_result_id>', methods=['GET', 'POST'])
@login_required
def view_weekly_result(weekly_result_id):
    weekly_result = WeeklyResult.query.get_or_404(weekly_result_id)
    return render_template('weekly-result-view.html', title='Result Summary', weekly_result=weekly_result)


# Route to update a weekly result
@app.route('/weekly-result/<int:weekly_result_id>/update', methods=['GET', 'POST'])
@login_required
def update_weekly_result(weekly_result_id):
    weekly_result = WeeklyResult.query.get_or_404(weekly_result_id)
    if current_user.role != 'admin':
        abort(403)
    form = WeeklyResultUpdateForm()
    if form.validate_on_submit():
        weekly_result.rank = form.rank.data
        weekly_result.points = form.points.data
        db.session.commit()
        flash(f"Results have been updated", 'success')
        return redirect(url_for('weekly_results'))
    elif request.method == 'GET':
        form.rank.data = weekly_result.rank
        form.points.data = weekly_result.points
    return render_template('weekly-result-update.html', title='Update Weekly Result', legend='Update Result', form=form, weekly_result=weekly_result)


# Route to delete a weekly result
@app.route('/weekly-result/<int:weekly_result_id>/delete', methods=['POST'])
@login_required
def delete_weekly_result(weekly_result_id):
    weekly_result = WeeklyResult.query.get_or_404(weekly_result_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(weekly_result)
    db.session.commit()
    flash(f"Result has been deleted", 'success')
    return redirect(url_for('weekly_results'))


# Route to show the weekly results
@app.route('/weekly-results')
def weekly_results():
    weekly_results = WeeklyResult.query.filter_by(week=session['week_num']).order_by(WeeklyResult.rank).all()
    return render_template('weekly-results.html', title='Weekly Results', weekly_results=weekly_results)


# Route to create a weekly standing
@app.route('/standing-entry', methods=['GET', 'POST'])
@login_required
def standing_entry():
    form = WeeklyStandingForm()
    if form.validate_on_submit():
        standing_entry = WeeklyStanding(week=int(session['week_num']), user_id=int(form.user.data), rank=form.rank.data, points=form.points.data, wins=form.wins.data)
        db.session.add(standing_entry)
        db.session.commit()
        flash("You have added a weekly standing.", 'success')
        return redirect(url_for('standings'))
    return render_template('standings-entry.html', title='Weekly Standings Entry', legend='Create Standing', form=form)


# Route to view a weekly standing
@app.route('/weekly-standing/<int:weekly_standing_id>', methods=['GET', 'POST'])
@login_required
def view_weekly_standing(weekly_standing_id):
    weekly_standing = WeeklyStanding.query.get_or_404(weekly_standing_id)
    return render_template('weekly-standing-view.html', title='Standing Summary', weekly_standing=weekly_standing)


# Route to update a weekly standing
@app.route('/weekly-standing/<int:weekly_standing_id>/update', methods=['GET', 'POST'])
@login_required
def update_weekly_standing(weekly_standing_id):
    weekly_standing = WeeklyStanding.query.get_or_404(weekly_standing_id)
    if current_user.role != 'admin':
        abort(403)
    form = WeeklyStandingUpdateForm()
    if form.validate_on_submit():
        weekly_standing.rank = form.rank.data
        weekly_standing.points = form.points.data
        weekly_standing.wins = form.wins.data
        db.session.commit()
        flash(f"Standings have been updated", 'success')
        return redirect(url_for('standings'))
    elif request.method == 'GET':
        form.rank.data = weekly_standing.rank
        form.points.data = weekly_standing.points
        form.wins.data = weekly_standing.wins
    return render_template('weekly-standing-update.html', title='Update Weekly Standing', legend='Update Standing', form=form, weekly_standing=weekly_standing)


# Route to delete a weekly standing
@app.route('/weekly-standing/<int:weekly_standing_id>/delete', methods=['POST'])
@login_required
def delete_weekly_standing(weekly_standing_id):
    weekly_standing = WeeklyStanding.query.get_or_404(weekly_standing_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(weekly_standing)
    db.session.commit()
    flash(f"Standing has been deleted", 'success')
    return redirect(url_for('standings'))


# Route to show the weekly results
@app.route('/weekly-standings')
def standings():
    weekly_standings = WeeklyStanding.query.filter_by(week=session['week_num']).order_by(WeeklyStanding.rank).all()
    return render_template('standings.html', title='Weekly Standings', weekly_standings=weekly_standings)


# Route to upload a starting lineup csv
@app.route('/upload-starting-lineup', methods=['GET', 'POST'])
@login_required
def starting_lineup_upload():
    form = UploadForm()
    # Upload the file to uploads folder
    if form.validate_on_submit():
        if form.upload.data:
            file = form.upload.data
            f_name = secure_filename(file.filename)
            f_path = os.path.join(app.root_path, 'static/uploads', f_name)
            file.save(f_path)
            file = open(f_path, "r", encoding="utf-8")
            csv_reader = csv.reader(file, delimiter=',')
            # Skip the headers
            next(csv_reader)
            for row in csv_reader:
                # TODO: Add check for correct data in each field
                entry = StartingLineup(week=int(session['week_key']), position=int(row[0]), car_number=int(row[1]), driver=row[2], team=row[3])
                db.session.add(entry)
                db.session.commit()
            # Delete the file
            if os.path.exists(f_path):
                os.remove(f_path)
            flash(f"You have successfully uploaded the starting lineup for {session['week_name']}", 'success')
            return redirect(url_for('home'))
    else:
        return render_template('upload-file.html', title='Upload Starting Lineup', legend='Upload Starting Lineup', form=form)


# Route to show the starting lineup
@app.route('/starting-lineup')
def starting_lineup():
    # TODO: Add a route to view and update an individual starting lineup entry
    starting_lineup = StartingLineup.query.filter_by(week=session['week_key']).order_by(StartingLineup.position).all()
    return render_template('starting-lineup.html', title='Starting Lineup', starting_lineup=starting_lineup)


# Route to upload a race results csv
@app.route('/upload-race-results', methods=['GET', 'POST'])
@login_required
def race_results_upload():
    form = UploadForm()
    # Upload the file to uploads folder
    if form.validate_on_submit():
        if form.upload.data:
            file = form.upload.data
            f_name = secure_filename(file.filename)
            f_path = os.path.join(app.root_path, 'static/uploads', f_name)
            file.save(f_path)
            file = open(f_path, "r", encoding="utf-8")
            csv_reader = csv.reader(file, delimiter=',')
            # Skip the headers
            next(csv_reader)
            for row in csv_reader:
                # TODO: Add check for correct data in each field
                entry = Result(week=int(session['week_key']), finish_position=int(row[0]), driver=row[1], car_number=int(row[2]), make=row[3], laps=int(row[4]), start_position=int(row[5]), laps_led=int(row[6]), points=int(row[7]), bonus_points=int(row[8]))
                db.session.add(entry)
                db.session.commit()
            # Delete the file
            if os.path.exists(f_path):
                os.remove(f_path)
            flash(f"You have successfully uploaded the race results for {session['week_name']}", 'success')
            return redirect(url_for('home'))
    else:
        return render_template('upload-file.html', title='Upload Race Results', legend='Upload Race Results', form=form)


# Route to show the starting lineup
@app.route('/race-result')
def race_result():
    # TODO: Add a route to view and update an individual starting lineup entry
    race_results = Result.query.filter_by(week=session['week_key']).order_by(Result.finish_position).all()
    return render_template('race-result.html', title='Race Results', race_results=race_results)


# TODO add and admin page with links to register new users, enter schedule event, enter a driver entry, update a driver entry, enter results, enter/update weekly results, enter/update standings.