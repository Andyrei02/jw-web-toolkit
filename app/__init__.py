from flask import Flask
from app.config import Config
from app.extensions import db, migrate, login_manager
from app.utils.scheduler import start_scheduler

from app.blueprints.auth import auth_bp
from app.blueprints.main import main_bp
from app.blueprints.workbook import workbook_bp


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    print("Database URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    with app.app_context():
        start_scheduler()

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(workbook_bp)

    return app
