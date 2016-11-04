import random

from app import db
from app.Moderator.models import Moderator


class Transgression(db.Model):

    __tablename__ = 'transgression'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    moderator = db.Column(db.Integer, db.ForeignKey('moderator.id'))

    # Pending/Active status determined by Moderators
    status = db.Column(db.Boolean, default=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.moderator = self.get_random_moderator()

    def __repr__(self):
        return '<Transgression: %r>' % (self.title)

    def get_random_moderator(self):
        # only choose moderators that have the fewest pending
        # if all moderators have equal amount, choose any
        tgs = Transgression.query.all()
        mods = [mod.id for mod in Moderator.query.all()]
        if len(mods) == 0:
            return 0
        mods_pending_transgressions = {k: 0 for k in mods}
        for t in tgs:
            key = t.moderator
            if key in mods_pending_transgressions.keys():
                mods_pending_transgressions[key] += 1

        # Check to see if all mods have the same amount
        amount_for_each_mod = len(set(mods_pending_transgressions.values()))
        if amount_for_each_mod == 1:
            # All mods have same amount, choose any
            selected_mod = random.choice(mods)
        elif amount_for_each_mod > 1:
            # some mods have more than others, grab all mods with fewest
            smallest = min(mods_pending_transgressions.values())
            pruned_mods = [k for k, v in mods_pending_transgressions.items() if v == smallest]
            selected_mod = random.choice(pruned_mods)
        return selected_mod
