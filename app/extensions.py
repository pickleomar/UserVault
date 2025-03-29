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
login_manager.session_protection = "strong"
csrf = CSRFProtect()

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User #Avoids circular imports
    return User.query.get(user_id)
