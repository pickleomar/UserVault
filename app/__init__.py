from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from werkzeug.datastructures import MultiDict
from urllib.parse import parse_qs, urlencode
import werkzeug.urls
import werkzeug.routing
from .extensions import bcrypt, csrf 

# Apply Werkzeug patches before any Flask component imports
def patched_url_decode(query_string):
    return MultiDict(parse_qs(query_string.decode("utf-8")))

def patched_url_encode(query):
    return urlencode(query, doseq=True)

# Monkey-patch Werkzeug
werkzeug.urls.url_decode = patched_url_decode
werkzeug.urls.url_encode = patched_url_encode
werkzeug.routing.url_encode = patched_url_encode

from .config import Config
from .extensions import db, login_manager, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.controllers.auth.routes import auth_bp 
    from app.controllers.home.routes import home_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    # Jinja2 datetime filter
    def format_datetime(value, fmt="%d-%m-%Y"):
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return value.strftime(fmt)
    
    app.jinja_env.filters['datetimeformat'] = format_datetime

    # Security headers middleware
    @app.after_request
    def add_security_headers(response):
        #response.headers['Content-Security-Policy'] = "default-src 'self' https://cdn.jsdelivr.net; script-src 'self' https://cdn.jsdelivr.net; style-src 'self' https://cdn.jsdelivr.net;"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

    return app