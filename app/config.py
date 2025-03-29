import os 
from dotenv import load_dotenv


load_dotenv()

class Config: 
    SECRET_KEY= os.getenv('SECRET_KEY', 'D4f4UltS3ssIonK3Y')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL','postgresql://user:password@localhost/db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #For Production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

