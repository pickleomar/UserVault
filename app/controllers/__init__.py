# Create app/controllers/__init__.py
from .auth.routes import auth_bp
from .home.routes import home_bp

__all__ = ['auth_bp', 'home_bp']