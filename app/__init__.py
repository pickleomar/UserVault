from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager
from flask_migrate import Migrate 

migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    #Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    #blueprints registration
    from app.controllers.auth.routes import auth_bp 
    from app.controllers.home.routes import home_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    return app