from app import db


class Transgression(db.Model):

    __tablename__ = 'transgression'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Pending/Active status determined by Moderators
    status = db.Column(db.Boolean, default=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Transgression: %r>' % (self.title)
