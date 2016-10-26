import os
import unittest

from flask import url_for

from app import app, db
from app.Moderator.models import Moderator
from config import BASE_DIR


class AuthTestCase(unittest.TestCase):
    name = 'tester'
    email = 'tester@test.test'
    password = 'tester1234'

    def setUp(self):
        self.app = app.test_client()

        # Configure our app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.db')
        app.test_request_context().push()

        # Refresh testing database for each test
        db.session.close()
        db.drop_all()
        db.create_all()

        # Create moderator for use in tests
        mod = Moderator.create(self.name, self.email, self.password)
        db.session.add(mod)
        db.session.commit()

    # HELPERS
    def login(self, should_follow = True):
        res = self.app.post(
            url_for('mods.login'),
            data=dict(
                email=self.email,
                password=self.password),
            follow_redirects=should_follow)
        return res

    def test_pending_page_requires_login(self):
        response = self.app.get(url_for('mods.pending'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('private/login', response.location)

    def test_create_page_requires_login(self):
        response = self.app.get(url_for('mods.create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('private/login', response.location)

    def test_logout_route_requires_login(self):
        response = self.app.get(url_for('mods.logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('private/login', response.location)

    def test_user_redirected_to_pending_after_login(self):
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello tester', response.data)

    def test_authenticated_user_can_navigate_to_create(self):
        self.login()
        response = self.app.get(url_for('mods.create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Create', response.data)

    def test_authenticated_user_is_logged_out(self):
        self.login()
        response = self.app.get(url_for('mods.logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('private/login', response.location)

    # FLASH MESSAGES

    def test_logged_out_message_appears_after_logout(self):
        self.login()
        response = self.app.get(url_for('mods.logout'), follow_redirects=True)
        self.assertIn('logged out!', response.data)

    def test_login_err_shows_after_failed_login(self):
        response = self.app.post(
            url_for('mods.login'),
            data=dict(
                email='nope@nope.com',  # nope.jpg
                password='NOPE'),
            follow_redirects=True)
        self.assertIn('Your email or password is incorrect!', response.data)

