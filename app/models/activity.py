from datetime import datetime
from app.extensions import db

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp_str = db.Column(db.String)  # If stored as string
    
    @property
    def timestamp(self):
        return datetime.strptime(self.timestamp_str, "%Y-%m-%d %H:%M:%S")