from wtgnc import db, bcrypt, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
# For password reset tokens
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create database models/classes
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(20), nullable=False)
    user_last_name = db.Column(db.String(20), nullable=False)
    display_name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    profile_image = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    weekly_result = db.relationship('WeeklyResult', backref='name', lazy='dynamic')
    weekly_standing = db.relationship('WeeklyStanding', backref='name', lazy='dynamic')

    # Function to hash the password with bcrypt
    def set_pw(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Function to check the password hash with bcrypt
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # Generate a password reset JSON token that has a 30 minute expiration
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.user_first_name}', '{self.user_last_name}', '{self.display_name}', " \
            f"'{self.email}', '{self.role}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_id = db.Column(db.Integer, nullable=False)
    week_str = db.Column(db.String(30), nullable=False)
    track = db.Column(db.String(30), nullable=False)
    race = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weekly_result = db.relationship('WeeklyResult', backref='week_result', lazy='dynamic')
    weekly_standing = db.relationship('WeeklyStanding', backref='week_standing', lazy='dynamic')

    def __repr__(self):
        return f"Event('{self.week_str}', '{self.track}', '{self.race}', '{self.date}')"


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, db.ForeignKey('event.id'))
    car_number = db.Column(db.Integer, nullable=False)
    driver = db.Column(db.String(30), nullable=False)
    sponsor = db.Column(db.String(30), nullable=False)
    make = db.Column(db.String(10), nullable=False)
    team = db.Column(db.String(30), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"Driver('{self.car_number}', '{self.driver}', '{self.sponsor}'," \
            f"'{self.make}', '{self.team}')"


class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, db.ForeignKey('event.id'))
    display_name = db.Column(db.String(30), nullable=False)
    driver_1 = db.Column(db.String(30), nullable=False)
    driver_2 = db.Column(db.String(30), nullable=False)
    driver_3 = db.Column(db.String(30), nullable=False)
    driver_4 = db.Column(db.String(30), nullable=False)
    make = db.Column(db.String(10), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    active = db.Column(db.Boolean, nullable=False, default=True, server_default='False')
    visible = db.Column(db.Boolean, nullable=False, default=False, server_default='False')

    def __repr__(self):
        return f"Pick('{self.week}', '{self.display_name}', '{self.driver_1}', '{self.driver_2}'," \
            f"'{self.driver_3}', '{self.make}')"


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, db.ForeignKey('event.id'))
    finish_position = db.Column(db.Integer, nullable=False)
    driver = db.Column(db.String(30), nullable=False)
    car_number = db.Column(db.Integer, nullable=False)
    make = db.Column(db.String(10), nullable=False)
    laps = db.Column(db.Integer, nullable=False)
    start_position = db.Column(db.Integer, nullable=False)
    laps_led = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    bonus_points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Result('{self.week}', '{self.car_number}', '{self.driver}', '{self.points}')"


class StartingLineup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, db.ForeignKey('event.id'))
    position = db.Column(db.Integer, nullable=False)
    car_number = db.Column(db.Integer, nullable=False)
    driver = db.Column(db.String(30), nullable=False)
    team = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Result('{self.week}', '{self.position}', '{self.car_number}', '{self.driver}')"


class WeeklyResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rank = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Result('{self.week}', '{self.user_id}', '{self.rank}', '{self.points}')"


class WeeklyStanding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, db.ForeignKey('event.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rank = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    wins = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Result('{self.week}', '{self.user_id}', '{self.user}', '{self.rank}', '{self.points}', '{self.wins}')"


class Make(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Make('{self.make}')"