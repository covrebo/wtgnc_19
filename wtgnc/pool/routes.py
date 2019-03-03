from flask_login import current_user, login_required
from wtgnc import db
from flask import render_template, url_for, session, flash, redirect, request, abort, Blueprint
from wtgnc.pool.forms import PickSelectionForm, WeeklyResultForm, WeeklyStandingForm, WeeklyResultUpdateForm, WeeklyStandingUpdateForm
from wtgnc.models import User, Pick, WeeklyResult, WeeklyStanding
from wtgnc.pool.utils import generate_entry_list, generate_make_list, generate_user_list

pool = Blueprint('pool', __name__, template_folder='templates')


# Route to submit weekly driver roster
@pool.route('/pick-page', methods=['GET', 'POST'])
@login_required
def pick_page():
    # TODO add modal to the page to confirm which week they are pick for
    form = PickSelectionForm()
    form.pick_1.choices = generate_entry_list()
    form.pick_2.choices = generate_entry_list()
    form.pick_3.choices = generate_entry_list()
    form.pick_4.choices = generate_entry_list()
    form.make.choices = generate_make_list()
    if form.validate_on_submit():
        pick_check = Pick.query.filter_by(week=session['week_num'], user_id=current_user.id).first()
        if pick_check:
            flash(f"Sorry, you have already submitted picks for {session['week_name']}.  Please visit the account page to update your picks or select a different week.", 'info')
            redirect(url_for('pool.pick_page'))
        else:
            picks = Pick(week=session['week_key'], display_name=current_user.display_name, driver_1=form.pick_1.data,
                         driver_2=form.pick_2.data, driver_3=form.pick_3.data, driver_4=form.pick_4.data,
                         make=form.make.data, user_id=current_user.id)
            db.session.add(picks)
            db.session.commit()
            flash(f"You have submitted picks for {session['week_name']}.  Good Luck!", 'success')
            return redirect(url_for('pool.picks_summary'))
    return render_template('pool/pick-page.html', title='Pick Page', form=form)


# Route to view individual roster
@pool.route('/picks/<int:pick_id>', methods=['GET', 'POST'])
@login_required
def picks_view(pick_id):
    picks = Pick.query.get_or_404(pick_id)
    return render_template('pool/picks-view.html', title='Picks Summary', picks=picks)


# Route to update a pick
@pool.route('/picks/<int:pick_id>/update', methods=['GET', 'POST'])
@login_required
def update_picks(pick_id):
    picks = Pick.query.get_or_404(pick_id)
    if current_user.id != picks.user_id:
        abort(403)
    form = PickSelectionForm()
    form.pick_1.choices = generate_entry_list()
    form.pick_2.choices = generate_entry_list()
    form.pick_3.choices = generate_entry_list()
    form.pick_4.choices = generate_entry_list()
    form.make.choices = generate_make_list()
    if form.validate_on_submit():
        picks.driver_1 = form.pick_1.data
        picks.driver_2 = form.pick_2.data
        picks.driver_3 = form.pick_3.data
        picks.driver_4 = form.pick_4.data
        picks.make = form.make.data
        db.session.commit()
        flash(f"You have updated your picks!", 'success')
        return redirect(url_for('pool.picks_summary'))
    elif request.method == 'GET':
        form.pick_1.data = picks.driver_1
        form.pick_2.data = picks.driver_2
        form.pick_3.data = picks.driver_3
        form.pick_4.data = picks.driver_4
        form.make.data = picks.make
    return render_template('pool/picks-update.html', title='Update Picks', legend='Update Picks', form=form, picks=picks)


# Route to delete a pick
@pool.route('/picks/<int:pick_id>/delete', methods=['POST'])
@login_required
def delete_pick(pick_id):
    picks = Pick.query.get_or_404(pick_id)
    if current_user.id != picks.user_id:
        abort(403)
    db.session.delete(picks)
    db.session.commit()
    flash(f"Picks have been deleted", 'success')
    return redirect(url_for('pool.picks_summary'))


# Route to deactivate a pick so user cannot update picks
@pool.route('/picks/<int:pick_id>/active', methods=['POST'])
@login_required
def change_active_pick(pick_id):
    picks = Pick.query.get_or_404(pick_id)
    if current_user.role != 'admin':
        abort(403)
    if picks.active == True:
        picks.active = False
        db.session.commit()
    else:
        picks.active = True
        db.session.commit()
    flash(f"Picks have been updated", 'success')
    return redirect(url_for('pool.admin_picks_summary'))


# Route to make a pick visible
@pool.route('/picks/<int:pick_id>/visible', methods=['POST'])
@login_required
def change_visible_pick(pick_id):
    picks = Pick.query.get_or_404(pick_id)
    if current_user.role != 'admin':
        abort(403)
    if picks.visible == True:
        picks.visible = False
        db.session.commit()
    else:
        picks.visible = True
        db.session.commit()
    flash(f"Picks have been updated", 'success')
    return redirect(url_for('pool.admin_picks_summary'))


# Route to display all weekly picks for admins
@pool.route('/admin-picks-summary')
@login_required
def admin_picks_summary():
    # TODO: Reorder picks by car number when they display
    if session.get('week_key'):
        picks = Pick.query.filter_by(week=session['week_key']).all()
        return render_template('pool/picks-admin.html', title='Pick Administration', picks=picks)
    else:
        flash("Please select a race to view the weekly picks.", 'info')
        return redirect(url_for('main.week_selection'))


# Route to display all weekly picks for users
@pool.route('/picks-summary')
@login_required
def picks_summary():
    # TODO: Reorder picks by car number when they display
    if session.get('week_key'):
        picks = Pick.query.filter_by(week=session['week_key']).all()
        return render_template('pool/picks.html', title='Pick Summary', picks=picks)
    else:
        flash("Please select a race to view the weekly picks.", 'info')
        return redirect(url_for('main.week_selection'))


# Route to the administration page
@pool.route('/admin')
@login_required
def admin():
    if current_user.role == 'admin':
        return render_template('pool/admin.html', title='Pool Admin')
    else:
        flash('You must be a commissioner to view the admin page!', 'warning')
        return redirect(url_for('main.home'))


# TODO: Create routes and templates to update and delete pool members - esp reset passwords for users without admin rights.
# Route to show the current list of pool members
@pool.route('/member-list')
def member_list():
    user_list = User.query.order_by(User.user_last_name).all()
    return render_template('pool/members.html', title='Member List', user_list=user_list)


# Route to create a weekly result
@pool.route('/weekly-result-entry', methods=['GET', 'POST'])
@login_required
def weekly_result_entry():
    form = WeeklyResultForm()
    form.user.choices = generate_user_list()
    if form.validate_on_submit():
        weekly_result = WeeklyResult(week=int(session['week_num']), user_id=int(form.user.data), rank=form.rank.data, points=form.points.data)
        db.session.add(weekly_result)
        db.session.commit()
        flash("You have added a weekly result.", 'success')
        return redirect(url_for('pool.weekly_results'))
    return render_template('pool/weekly-result-entry.html', title='Weekly Result Entry', legend='Create Result', form=form)


# Route to view a weekly result
@pool.route('/weekly-result/<int:weekly_result_id>', methods=['GET', 'POST'])
@login_required
def view_weekly_result(weekly_result_id):
    weekly_result = WeeklyResult.query.get_or_404(weekly_result_id)
    return render_template('pool/weekly-result-view.html', title='Result Summary', weekly_result=weekly_result)


# Route to update a weekly result
@pool.route('/weekly-result/<int:weekly_result_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('pool.weekly_results'))
    elif request.method == 'GET':
        form.rank.data = weekly_result.rank
        form.points.data = weekly_result.points
    return render_template('pool/weekly-result-update.html', title='Update Weekly Result', legend='Update Result', form=form, weekly_result=weekly_result)


# Route to delete a weekly result
@pool.route('/weekly-result/<int:weekly_result_id>/delete', methods=['POST'])
@login_required
def delete_weekly_result(weekly_result_id):
    weekly_result = WeeklyResult.query.get_or_404(weekly_result_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(weekly_result)
    db.session.commit()
    flash(f"Result has been deleted", 'success')
    return redirect(url_for('pool.weekly_results'))


# Route to show the weekly results
@pool.route('/weekly-results')
@login_required
def weekly_results():
    if session.get('week_num'):
        weekly_results = WeeklyResult.query.filter_by(week=session['week_num']).order_by(WeeklyResult.rank).all()
        return render_template('pool/weekly-results.html', title='Weekly Results', weekly_results=weekly_results)
    else:
        flash("Please select a race to view the weekly results.", 'info')
        return redirect(url_for('main.week_selection'))


# Route to create a weekly standing
@pool.route('/standing-entry', methods=['GET', 'POST'])
@login_required
def standing_entry():
    form = WeeklyStandingForm()
    form.user.choices = generate_user_list()
    if form.validate_on_submit():
        standing_entry = WeeklyStanding(week=int(session['week_num']), user_id=int(form.user.data), rank=form.rank.data, points=form.points.data, wins=form.wins.data)
        db.session.add(standing_entry)
        db.session.commit()
        flash("You have added a weekly standing.", 'success')
        return redirect(url_for('pool.standings'))
    return render_template('pool/standings-entry.html', title='Weekly Standings Entry', legend='Create Standing', form=form)


# Route to view a weekly standing
@pool.route('/weekly-standing/<int:weekly_standing_id>', methods=['GET', 'POST'])
@login_required
def view_weekly_standing(weekly_standing_id):
    weekly_standing = WeeklyStanding.query.get_or_404(weekly_standing_id)
    return render_template('pool/weekly-standing-view.html', title='Standing Summary', weekly_standing=weekly_standing)


# Route to update a weekly standing
@pool.route('/weekly-standing/<int:weekly_standing_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('pool.standings'))
    elif request.method == 'GET':
        form.rank.data = weekly_standing.rank
        form.points.data = weekly_standing.points
        form.wins.data = weekly_standing.wins
    return render_template('pool/weekly-standing-update.html', title='Update Weekly Standing', legend='Update Standing', form=form, weekly_standing=weekly_standing)


# Route to delete a weekly standing
@pool.route('/weekly-standing/<int:weekly_standing_id>/delete', methods=['POST'])
@login_required
def delete_weekly_standing(weekly_standing_id):
    weekly_standing = WeeklyStanding.query.get_or_404(weekly_standing_id)
    if current_user.role != 'admin':
        abort(403)
    db.session.delete(weekly_standing)
    db.session.commit()
    flash(f"Standing has been deleted", 'success')
    return redirect(url_for('pool.standings'))


# Route to show the weekly results
@pool.route('/weekly-standings')
@login_required
def standings():
    if session.get('week_num'):
        weekly_standings = WeeklyStanding.query.filter_by(week=session['week_num']).order_by(WeeklyStanding.rank).all()
        return render_template('pool/standings.html', title='Weekly Standings', weekly_standings=weekly_standings)
    else:
        flash("Please select a race to view the weekly standings.", 'info')
        return redirect(url_for('main.week_selection'))