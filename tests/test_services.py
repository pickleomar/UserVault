import unittest
import werkzeug.urls
from urllib.parse import parse_qs
from werkzeug.datastructures import MultiDict

# Apply patch first
def werkzeug_url_decode(query_string):
    return MultiDict(parse_qs(query_string.decode("utf-8"))  )# Safe decoding

werkzeug.urls.url_decode = werkzeug_url_decode

from datetime import datetime
from app import create_app
from app.extensions import db
from app.models.user import User
from app.services.user_service import UserService

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        self.user = User(
            username='testuser',
            email='test@example.com',
            password='securepassword'
        )
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_complexity(self):
        weak_passwords = [
            'password',
            '12345678',
            'Test123',
            'Secure!'
        ]
        
        for pwd in weak_passwords:
            with self.subTest(password=pwd):
                result = UserService.change_password(
                    self.user, 
                    'securepassword',
                    pwd
                )
                self.assertFalse(result, f"Weak password accepted: {pwd}")

    def test_brute_force_protection(self):
        # Test failed login attempts
        for _ in range(5):
            UserService.authenticate('test@example.com', 'wrongpassword')
        
        result = UserService.authenticate('test@example.com', 'securepassword')
        self.assertFalse(result, "Brute force protection failed")

    def test_session_validation(self):
        valid_token = UserService.generate_session_token(self.user)
        invalid_token = valid_token[:-4] + 'XXXX'
        
        self.assertTrue(UserService.validate_session_token(valid_token))
        self.assertFalse(UserService.validate_session_token(invalid_token))