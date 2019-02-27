from flask_login import login_user, current_user, logout_user, login_required
from wtgnc import db
from flask import render_template, url_for, session, flash, redirect, request, Blueprint
from wtgnc.models import User, Pick, WeeklyResult, WeeklyStanding
from wtgnc.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetTokenForm, PasswordResetForm
from wtgnc.users.utils import send_reset_email, save_picture

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.is_authenticated and current_user.role != 'admin':
        flash('You are already logged in as a registered user.  Contact a commissioner to register a new account.', 'info')
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(user_first_name=form.user_first_name.data, user_last_name=form.user_last_name.data, display_name=form.display_name.data, email=form.email.data, role=form.role.data)
        user.set_pw(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.display_name.data}!', 'success')
        return redirect(url_for('main.home'))
    return render_template('users/register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # TODO: Does this protect against SQL injection?
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"{current_user.display_name} successfully logged in.", 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.week_selection'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    if session.get('week_num') != None:
        session.pop('week_num')
    if session.get('week_name') != None:
        session.pop('week_name')
    if session.get('week_key') != None:
        session.pop('week_key')
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))


# Route to the user account page
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.user_first_name.data = current_user.user_first_name
        form.user_last_name.data = current_user.user_last_name
        form.display_name.data = current_user.display_name
        form.email.data = current_user.email
    image_file = url_for('static', filename=f"profile_pics/{current_user.profile_image}")
    # TODO: Add statistics to account - driver popularity, weekly avg points, wins, etc.
    picks = Pick.query.filter_by(user_id=current_user.id).order_by(Pick.week).all()
    results = WeeklyResult.query.filter_by(user_id=current_user.id).order_by(WeeklyResult.week).all()
    standings = WeeklyStanding.query.filter_by(user_id=current_user.id).order_by(WeeklyStanding.week).all()
    return render_template('users/account.html', title='Account', legend='Account Info', image_file=image_file, form=form, picks=picks, results=results, standings=standings)


# Route to request a password reset email
@users.route('/request-password-reset', methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.home'))
    form = RequestResetTokenForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", 'info')
        return redirect(url_for('users.login'))
    return render_template('users/request-password-reset.html', title='Request a Password Reset', legend="Request a Password Reset", form=form)


# Route to verify a token and reset the password
@users.route('/password-reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This link is invalid or has expired.  Please request another.', 'warning')
        return redirect(url_for('users.request_password_reset'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_pw(form.password.data)
        db.session.commit()
        flash(f'Your password has been updated.  You can now login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/reset-password.html', title='Reset Password', legend='Reset Password', form=form)