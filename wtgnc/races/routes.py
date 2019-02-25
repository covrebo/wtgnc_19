import os
import csv
from io import StringIO
from flask_login import current_user, login_required
from wtgnc import db
from flask import render_template, url_for, session, flash, redirect, request, abort, Blueprint, current_app
from werkzeug.utils import secure_filename
from wtgnc.models import Driver, Event, Result, StartingLineup, Make
from wtgnc.races.forms import EntryForm, EventForm, UploadForm, MakeForm
from wtgnc.races.utils import generate_make_list

races = Blueprint('races', __name__, template_folder='templates')


# Route to upload an entry list csv
@races.route('/upload-entry-list', methods=['GET', 'POST'])
@login_required
def entry_list_upload():
    form = UploadForm()
    if form.validate_on_submit():
        if form.upload.data:
            file = form.upload.data
            file_data = StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.reader(file_data, delimiter=',')
            # Skip the headers
            next(csv_reader)
            for row in csv_reader:
                # TODO: Add check for correct data in each field
                entry = Driver(week=int(session['week_key']), car_number=int(row[0]), driver=row[1], sponsor=row[2], make=row[3], team=row[4])
                db.session.add(entry)
                db.session.commit()
            flash('You have successfully uploaded the entry list', 'success')
            return redirect(url_for('races.entry_list'))
    else:
        return render_template('races/upload-file.html', title='Upload Entry List', legend='Upload Entry List', form=form)


# Route to create a driver entry
@races.route('/driver-entry', methods=['GET', 'POST'])
@login_required
def driver_entry():
    form = EntryForm()
    form.make.choices = generate_make_list()
    if form.validate_on_submit():
        driver = Driver(week=int(session['week_num']), car_number=form.car_number.data, driver=form.driver.data, sponsor=form.sponsor.data, make=form.make.data, team=form.team.data)
        db.session.add(driver)
        db.session.commit()
        flash(f"You have added {form.driver.data}.", 'success')
        return redirect(url_for('races.entry_list'))
    return render_template('races/driver-entry.html', title='Driver Entry', legend='Create Driver', form=form)


# Route to view a driver entry
@races.route('/driver/<int:driver_id>', methods=['GET', 'POST'])
@login_required
def driver(driver_id):
    # TODO: Add a performance summary for each race to the driver page
    # TODO: Add an popularity measure, average start, average finish, average stage points, and average total points stat to each driver.
    driver = Driver.query.get_or_404(driver_id)
    return render_template('races/driver.html', title='Driver Summary', driver=driver)


# Route to update a driver entry
@races.route('/driver/<int:driver_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('races.entry_list'))
    elif request.method == 'GET':
        form.car_number.data = driver.car_number
        form.driver.data = driver.driver
        form.sponsor.data = driver.sponsor
        form.make.data = driver.make
        form.team.data = driver.team
        form.active.data = driver.active
    return render_template('races/driver-entry.html', title='Driver Update', legend='Update Driver', form=form)


# Route to delete a driver entry
@races.route('/driver/<int:driver_id>/delete', methods=['POST'])
@login_required
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(driver)
    db.session.commit()
    flash(f"Driver has been deleted", 'success')
    return redirect(url_for('races.entry_list'))


# Route to show the current entry list
@races.route('/entry-list')
def entry_list():
    entry_list = Driver.query.filter_by(week=session['week_key']).order_by(Driver.car_number).all()
    return render_template('races/entry-list.html', title='Entry List', entry_list=entry_list)


# Route to create a race entry
@races.route('/race-event', methods=['GET', 'POST'])
@login_required
def race_event():
    # TODO: Style the date selection field properly
    form = EventForm()
    if form.validate_on_submit():
        event = Event(week_id=form.week.data, week_str=f"Week {form.week.data} - {form.track.data}", track=form.track.data, race=form.race.data, date=form.date.data)
        db.session.add(event)
        db.session.commit()
        flash(f"You have added the {form.race.data}.", 'success')
        return redirect(url_for('races.schedule'))
    return render_template('races/race-event.html', title='Race Event', legend='Create Race Event', form=form)


# Route to view a race entry
@races.route('/race/<int:race_id>', methods=['GET', 'POST'])
@login_required
def race(race_id):
    race = Event.query.get_or_404(race_id)
    return render_template('races/race.html', title='Race Summary', race=race)


# Route to update a race entry
@races.route('/race/<int:race_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('races.schedule'))
    elif request.method == 'GET':
        form.week.data = race.week_id
        form.track.data = race.track
        form.race.data = race.race
        form.date.data = race.date
    return render_template('races/race-event.html', title='Race Update', legend='Update Race', form=form)


# Route to delete a race entry
@races.route('/race/<int:race_id>/delete', methods=['POST'])
@login_required
def delete_race(race_id):
    race = Event.query.get_or_404(race_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(race)
    db.session.commit()
    flash(f"Race has been deleted", 'success')
    return redirect(url_for('races.schedule'))


# Route to show the current schedule
@races.route('/schedule')
def schedule():
    schedule = Event.query.all()
    return render_template('races/schedule.html', title='Schedule', schedule=schedule)


# Route to upload a starting lineup csv
@races.route('/upload-starting-lineup', methods=['GET', 'POST'])
@login_required
def starting_lineup_upload():
    form = UploadForm()
    # Upload the file to uploads folder
    if form.validate_on_submit():
        if form.upload.data:
            file = form.upload.data
            file_data = StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.reader(file_data, delimiter=',')
            # Skip the headers
            next(csv_reader)
            for row in csv_reader:
                # TODO: Add check for correct data in each field
                entry = StartingLineup(week=int(session['week_key']), position=int(row[0]), car_number=int(row[1]), driver=row[2], team=row[3])
                db.session.add(entry)
                db.session.commit()
            flash(f"You have successfully uploaded the starting lineup for {session['week_name']}", 'success')
            return redirect(url_for('races.starting_lineup'))
    else:
        return render_template('races/upload-file.html', title='Upload Starting Lineup', legend='Upload Starting Lineup', form=form)


# Route to show the starting lineup
@races.route('/starting-lineup')
def starting_lineup():
    # TODO: Add a route to view and update an individual starting lineup entry
    starting_lineup = StartingLineup.query.filter_by(week=session['week_key']).order_by(StartingLineup.position).all()
    return render_template('races/starting-lineup.html', title='Starting Lineup', starting_lineup=starting_lineup)


# Route to upload a race results csv
@races.route('/upload-race-results', methods=['GET', 'POST'])
@login_required
def race_results_upload():
    form = UploadForm()
    # Upload the file to uploads folder
    if form.validate_on_submit():
        if form.upload.data:
            file = form.upload.data
            file_data = StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_reader = csv.reader(file_data, delimiter=',')
            # Skip the headers
            next(csv_reader)
            for row in csv_reader:
                # TODO: Add check for correct data in each field
                entry = Result(week=int(session['week_key']), finish_position=int(row[0]), driver=row[1], car_number=int(row[2]), make=row[3], laps=int(row[4]), start_position=int(row[5]), laps_led=int(row[6]), points=int(row[7]), bonus_points=int(row[8]))
                db.session.add(entry)
                db.session.commit()
            flash(f"You have successfully uploaded the race results for {session['week_name']}", 'success')
            return redirect(url_for('races.race_result'))
    else:
        return render_template('races/upload-file.html', title='Upload Race Results', legend='Upload Race Results', form=form)


# Route to show the race results
@races.route('/race-result')
def race_result():
    # TODO: Add a route to view and update an individual starting lineup entry
    race_results = Result.query.filter_by(week=session['week_key']).order_by(Result.finish_position).all()
    return render_template('races/race-result.html', title='Race Results', race_results=race_results)


# Route to create a make
@races.route('/make-entry', methods=['GET', 'POST'])
@login_required
def make_entry():
    form = MakeForm()
    if form.validate_on_submit():
        make = Make(make=form.make.data)
        db.session.add(make)
        db.session.commit()
        flash(f"You have added {form.make.data}.", 'success')
        # TODO: Change to redirect to make list when done
        return redirect(url_for('pool.admin'))
    return render_template('races/make-entry.html', title='Make Entry', legend='Create Make', form=form)


# Route to view a make entry
@races.route('/make/<int:make_id>', methods=['GET', 'POST'])
@login_required
def view_make(make_id):
    make = Make.query.get_or_404(make_id)
    return render_template('races/make-view.html', title='Make Summary', make=make)


# Route to update a make entry
@races.route('/make/<int:make_id>/update', methods=['GET', 'POST'])
@login_required
def update_make(make_id):
    make = Make.query.get_or_404(make_id)
    if current_user.role != 'admin':
        abort(403)
    form = MakeForm()
    if form.validate_on_submit():
        make.make = form.make.data
        db.session.commit()
        flash(f"Make has been updated.", 'success')
        return redirect(url_for('races.make'))
    elif request.method == 'GET':
        form.make.data = make.make
    return render_template('races/make-entry.html', title='Make Update', legend='Update Make', form=form)


# Route to delete a race entry
@races.route('/make/<int:make_id>/delete', methods=['POST'])
@login_required
def delete_make(make_id):
    make = Make.query.get_or_404(make_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(make)
    db.session.commit()
    flash(f"Make has been deleted", 'success')
    return redirect(url_for('races.make_list'))


# TODO: Implement moment so dates display correctly
# Route to show the current schedule
@races.route('/make')
def make_list():
    make_list = Make.query.all()
    return render_template('races/make-list.html', title='Make List', make_list=make_list)

# TODO: add routes and templates to view make list, update make, and delete makes
