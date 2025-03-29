from app.extensions import db 
from flask_login import UserMixin
from datetime import datetime 
import uuid
from sqlalchemy.dialects.postgresql import UUID

class User(db.Model, UserMixin):

    __tablename__ = 'users'
    
    #We use UUID here for scalability and 
    #for uniqueness across different dbs + harder to guess ids for more security
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email= db.Column(db.String(120), unique=True, nullable=True)
    username= db.Column(db.String(80), nullable= False)
    password_hash=db.Column(db.String(128), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)  
    bio = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #For debugging 
    def __repr__(self):
        return f'<User {self.username}>'