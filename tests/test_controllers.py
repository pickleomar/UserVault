import unittest
from flask import url_for
from werkzeug.datastructures import MultiDict
from urllib.parse import parse_qs
import werkzeug.urls

# Apply patch before any Flask imports
def werkzeug_url_decode(query_string):
    return MultiDict(parse_qs(query_string.decode("utf-8")))# Safe decoding

werkzeug.urls.url_decode = werkzeug_url_decode

from app import create_app
from app.extensions import db
from app.models.user import User

class TestControllers(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config='testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create test user
        self.user = User(
            username='testuser',
            email='test@example.com',
            password='securepassword'
        )
        db.session.add(self.user)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_security_headers(self):
        response = self.client.get('/')
        self.assertEqual(response.headers['Content-Security-Policy'], "default-src 'self'")
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')

    def test_authentication_flow(self):
        # Test login redirect
        resp = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Login', resp.data)

        # Test successful login
        with self.client:
            resp = self.client.post('/auth/login', data={
                'email': 'test@example.com',
                'password': 'securepassword'
            }, follow_redirects=True)
            self.assertIn(b'Dashboard', resp.data)
            self.assertEqual(resp.status_code, 200)

    def test_csrf_protection(self):
        resp = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'securepassword'
        })
        self.assertEqual(resp.status_code, 400)