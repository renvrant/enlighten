import os
import unittest

from flask import url_for

from app import app, db
from app.Moderator.models import Moderator
from config import BASE_DIR



class BaseTestCase(unittest.TestCase):
    name = 'tester'
    email = 'tester@test.test'
    password = 'tester1234'

    story_title = 'test incident title'
    story_content = 'test incident body'

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
        response = self.app.post(
            url_for('mods.login'),
            data=dict(
                email=self.email,
                password=self.password),
            follow_redirects=should_follow)
        return response

    def create_incident(self):
        response = self.app.post(
            url_for('story.share'),
            data=dict(
                title=self.story_title,
                content=self.story_content),
            follow_redirects=True)
        return response
