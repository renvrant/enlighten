from flask import url_for

from ..base.base_test_case import BaseTestCase


class AuthTestCase(BaseTestCase):

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
        self.assertIn('Hello, Tester!', response.data)

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

