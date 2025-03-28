from app.extensions import db 
from flask_login import UserMixin

import uuid
from sqlalchemy.dialects.postgresql import uuid

class User(db.Model, UserMixin):
    #We use UUID here for scalability and 
    #for uniqueness across different dbs + harder to guess ids for more security
    id= db.Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid4, unique=True, nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=True)
    username= db.Column(db.String(80), nullable= False)
    password_hash=db.Column(db.String(128), nullable=False)
