from flask import url_for

from app import db
from app.Moderator.models import Moderator
from app.Story.models import Story
from ..base.base_test_case import BaseTestCase


class ModeratorTestCase(BaseTestCase):

    # CONTROLLER

    def test_should_have_route_for_creating_moderators(self):
        self.login(True)
        response = self.app.get(url_for('mods.create'), follow_redirects=True)
        self.assertIn('Create!', response.data)

    def test_should_allow_moderator_to_approve_pending_test(self):
        self.login()
        self.create_incident()
        story = Story.query.filter_by(title=self.story_title).first()

        # Set pending status to approved
        status, title, content = True, self.story_title, self.story_content
        response = self.app.post(
            url_for('mods.edit_story', story_id=story.id),
            data=dict(
                title=title,
                content=content,
                status=status),
            follow_redirects=True)
        self.assertIn('Incident Approved', response.data)

        # Check to see if incident shows up
        response = self.app.get(url_for('story.index'), follow_redirects=True)
        self.assertIn(self.story_title, response.data)

    def test_should_not_allow_unassigned_user_to_approve_pending_story(self):
        # Create a new story
        self.create_incident()

        # Create a new user
        email, password = 'disposable@example.com', 'fnord'
        user = Moderator.create('disposable', email, password)
        db.session.add(user)
        db.session.commit()

        # Login as that user
        self.app.post(
            url_for('mods.login'),
            data=dict(
                email=email,
                password=password),
            follow_redirects=True)

        # Attempt to view edit page of pending story
        story = Story.query.filter_by(title=self.story_title).first()
        response = self.app.get(url_for('mods.edit_story', story_id=story.id),
                                follow_redirects=True)
        self.assertIn('You do not have permission to view this resource.', response.data)

    def test_should_be_able_to_create_another_moderator(self):
        self.login()

        # Get current moderator count
        total_mods = len(Moderator.query.all())

        # Attempt to create a moderator
        name, email = 'temp', 'temp@temp.temp'
        response = self.app.post(
            url_for('mods.create'),
            data=dict(
                name=name,
                email=email,
                password=name,
                confirm=name),
            follow_redirects=True)

        self.assertIn('Moderator created successfully!', response.data)
        new_total_mods = len(Moderator.query.all())
        self.assertGreater(new_total_mods, total_mods)
