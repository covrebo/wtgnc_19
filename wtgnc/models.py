from wtgnc import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin


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

    # Function to hash the password with bcrypt
    def set_pw(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Function to check the password hash with bcrypt
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

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

    def __repr__(self):
        return f"Pick('{self.week}', '{self.display_name}', '{self.driver_1}', '{self.driver_2}'," \
            f"'{self.driver_3}', '{self.make}')"


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, db.ForeignKey('event.id'))
    car_number = db.Column(db.Integer, nullable=False)
    driver = db.Column(db.String(30), nullable=False)
    points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Result('{self.week}', '{self.car_number}', '{self.driver}', '{self.points}')"


class Make(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Make('{self.make}')"