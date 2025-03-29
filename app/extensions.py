from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
# Initialize extensions
db = SQLAlchemy()
bcrypt= Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User  # Import inside function to avoid circular import
    return User.query.get(user_id)
