from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from wtgnc.users.routes import users
    from wtgnc.pool.routes import pool
    from wtgnc.races.routes import races
    from wtgnc.main.routes import main
    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(pool, url_prefix='/pool')
    app.register_blueprint(races, url_prefix='/races')
    app.register_blueprint(main)

    return app