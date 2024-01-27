# __init__.py
from flask import Flask
from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'your_secret_key'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from .routes.main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # Create tables if they don't exist
        db.create_all()

    return app
