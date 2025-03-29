import unittest
import werkzeug.urls
from urllib.parse import parse_qs
from werkzeug.datastructures import MultiDict

# Apply patch first
def werkzeug_url_decode(query_string):
    return MultiDict(parse_qs(query_string.decode("utf-8")) ) # Safe decoding

werkzeug.urls.url_decode = werkzeug_url_decode

from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_security(self):
        user = User(username='test', email='test@example.com')
        user.set_password('TestPassword123!')
        self.assertTrue(user.check_password('TestPassword123!'))
        self.assertFalse(user.check_password('wrongpassword'))
        self.assertNotEqual(user.password_hash, 'TestPassword123!')

    def test_session_timeout(self):
        user = User()
        original_token = user.get_auth_token()
        
        # Simulate time passing
        with self.app.test_request_context():
            user.last_login = datetime.utcnow() - timedelta(hours=2)
            new_token = user.get_auth_token()
            self.assertNotEqual(original_token, new_token)

    def test_activity_tracking(self):
        user = User()
        db.session.add(user)
        db.session.commit()
        
        initial_activity = user.last_activity
        user.update_activity()
        self.assertNotEqual(initial_activity, user.last_activity)