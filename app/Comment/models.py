from app import db


class Reply(db.Model):

    __tablename__ = 'reply'

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    reply_to = db.Column(db.Integer, db.ForeignKey('comment.id'))

    def __init__(self, comment_id, reply_to_id):
        self.comment_id = comment_id
        self.reply_to = reply_to_id

    def __repr__(self):
        return '<Reply to={}, from={}>'.format(self.reply_to, self.comment_id)


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True)
    body = db.Column(db.Text, nullable=False)
    is_moderator = db.Column(db.Boolean, default=False)
    story = db.Column(db.Integer, db.ForeignKey('story.id'))
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, title, body, is_moderator, story_id):
        self.title = title
        self.body = body
        self.is_moderator = is_moderator
        self.story = story_id

    def get_replies(self):
        replies = Reply.query.filter_by(reply_to=self.id).all()
        for reply in replies:
            comment = Comment.query.get(reply.comment_id)
            yield comment

    def get_date(self):
        return self.date_added.strftime('%A, %b %-d, %-I:%M %p')
