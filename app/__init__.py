from flask import Flask
from app.config import Config
from app.extensions import db, login_manager
from app.blueprints.auth import auth_bp
from app.blueprints.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    return app
