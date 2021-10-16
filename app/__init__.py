from flask import Flask
from flask_login import LoginManager

from .utils import db

login_manager = LoginManager()
db = db.db


def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings_module)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .portal import portal_bp
    app.register_blueprint(portal_bp)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app
