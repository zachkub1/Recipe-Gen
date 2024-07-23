from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)

    register_blueprints(app)
    configure_login_manager(app)
    initialize_database(app)

    return app

def register_blueprints(app):
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

def configure_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

def initialize_database(app):
    with app.app_context():
        if not database_exists(DB_NAME):
            db.create_all()
            print('Created Database!')

def database_exists(database_name):
    return os.path.exists(f'website/{database_name}')
