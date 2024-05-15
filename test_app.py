import unittest
from flask import current_app
from project import create_app, db
from project.models import User
from werkzeug.security import check_password_hash
from sqlalchemy import text


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": 'sqlite://'} )
        self.app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_homepage_redirect(self):
        response = self.client.get('/', follow_redirects = True)
        assert response.status_code == 200

    def test_registration_form(self):
        response = self.client.get('/signup')
        assert response.status_code == 200

    def test_no_access_to_profile(self):
        response = self.client.get('/profile', follow_redirects = True)
        assert 'login' in response.request.path.lower()

    def test_register_user(self):
        response = self.client.post('/signup', data = {
            'email' : 'user@test.com',
            'name' : 'test user',
            'password' : 'test123'
        }, follow_redirects = True)
        assert response.status_code == 200
        # should redirect to the login page
        assert response.request.path == '/login'

        # verify that user can now login
        response = self.client.post('/login', data = {
            'email' : 'user@test.com',
            'password' : 'test123'
        }, follow_redirects = True)
        assert response.status_code == 200
        html = response.get_data(as_text = True)
        assert 'test user' in html

    def test_hashed_passwords(self):
        response = self.client.post('/signup', data = {
            'email' : 'user@test.com',
            'name' : 'test user',
            'password' : 'test123'
        }, follow_redirects = True)
        assert response.status_code == 200
        # should redirect to the login page
        assert response.request.path == '/login'

        user = User.query.filter_by(email='user@test.com').first()
        assert user is not None
        assert check_password_hash(user.password, 'test123')

    def test_sql_injection(self):
        response = self.client.post('/signup', data={
            'email': 'user@test.com"; drop table user; -- ',
            'name': 'test user',
            'password': 'test123'
        }, follow_redirects=True)
        # Check that the table 'user' still exists
        user_count = db.session.execute(text('SELECT COUNT(*) FROM user')).scalar()
        assert user_count is not None

        assert response.status_code == 200

    def test_xss_vulnerability(self):
        bad_name = "<script>alert('XSS');</script>"
        self.client.post('/signup', data={'email': 'xss@test.com', 'name': bad_name, 'password': 'password123'},
                    follow_redirects=True)

        self.client.post('/login', data={'email': 'xss@test.com', 'password': 'password123'}, follow_redirects=True)
        response = self.client.get('/profile', follow_redirects=True)

        # If the response does not contain the unescaped script tag, it means our application is safe.
        assert bad_name not in response.get_data(as_text=True)


