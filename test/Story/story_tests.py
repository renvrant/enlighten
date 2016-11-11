from flask import url_for

from app import db
from app.Moderator.models import Moderator
from app.Story.models import Story

from test.base.base_test_case import BaseTestCase


class StoryTestCase(BaseTestCase):

    def test_should_be_able_to_create_a_story(self):
        total_tgs = len(Story.query.all())
        self.create_incident()
        new_total_tgs = len(Story.query.all())
        self.assertGreater(new_total_tgs, total_tgs)

    def test_should_randomly_assign_a_moderator_to_new_story(self):
        self.login()

        # Create an additional moderator
        self.app.post(
            url_for('mods.create'),
            data=dict(
                name='temp',
                email='temp@temp.temp',
                password='temp',
                confirm='temp'),
            follow_redirects=True)
        valid_mod_ids = [m.id for m in Moderator.query.all()]

        self.create_incident()
        tg = Story.query.first()
        self.assertIn(tg.moderator, valid_mod_ids)


    def test_should_prioritize_moderators_with_fewest_pending_stories(self):
        self.login()

        # Create a few stories
        self.create_incident()
        self.create_incident()
        self.create_incident()

        # Create a new moderator
        response = self.app.post(
            url_for('mods.create'),
            data=dict(
                name='temp',
                email='temp@temp.temp',
                password='temp',
                confirm='temp'),
            follow_redirects=True)
        mod = Moderator.query.filter_by(name='temp').first()

        # Create another incident
        self.create_incident()
        tgs = Story.query.filter_by(moderator=mod.id).all()
        self.assertEqual(len(tgs), 1)
        self.assertEqual(tgs[0].moderator, mod.id)
