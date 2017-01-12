import random

from app import db
from app.Moderator.models import Moderator
from app.Comment.models import Comment

class Story(db.Model):

    __tablename__ = 'story'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    moderator = db.Column(db.Integer, db.ForeignKey('moderator.id'))
    comments = db.Column(db.ARRAY(db.Integer), nullable=True, default=[])
    content_warning = db.Column(db.ARRAY(db.Integer), nullable=True, default=[])

    # Pending/Active status determined by Moderators
    status = db.Column(db.Boolean, default=False)
    allow_comments = db.Column(db.Boolean, default=False)
    content_warning = db.Column(db.Boolean, default=False)

    def __init__(self, title, content, allow_comments=False, content_warning=False):
        self.title = title
        self.content = content
        self.moderator = self.get_random_moderator()
        self.allow_comments = allow_comments
        self.content_warning = content_warning

    def __repr__(self):
        return '<Story: %r>' % (self.title)

    def get_comments(self):
        for comment_id in self.comments:
            comment = Comment.query.get(comment_id)
            yield comment

    def get_random_moderator(self):
        # only choose moderators that have the fewest pending
        # if all moderators have equal amount, choose any
        tgs = Story.query.all()
        mods = [mod.id for mod in Moderator.query.all()]
        if len(mods) == 0:
            return 0
        mods_pending_stories = {k: 0 for k in mods}
        for t in tgs:
            key = t.moderator
            if key in mods_pending_stories.keys():
                mods_pending_stories[key] += 1

        # Check to see if all mods have the same amount
        amount_for_each_mod = len(set(mods_pending_stories.values()))
        if amount_for_each_mod == 1:
            # All mods have same amount, choose any
            selected_mod = random.choice(mods)
        elif amount_for_each_mod > 1:
            # some mods have more than others, grab all mods with fewest
            smallest = min(mods_pending_stories.values())
            pruned_mods = [k for k, v in mods_pending_stories.items() if v == smallest]
            selected_mod = random.choice(pruned_mods)
        return selected_mod
