from flask import render_template, redirect, url_for, abort, Blueprint, \
                  flash
from flask_login import login_required, logout_user, login_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.Story.forms import CreateStoryForm
from app.Story.models import Story
from app.Comment.models import Comment, Reply
from app.Comment.forms import CommentForm
from app.Moderator.models import Moderator


story = Blueprint('story', __name__, url_prefix='/common')


@story.route('/')
def index():
    stories = Story.query.filter_by(status=True)

    # Uncomment this code to see which mods have pending from the index screen
    # for development only

    all_stories = Story.query.all()
    mods = [mod for mod in Moderator.query.all()]
    ps = {k.id: 0 for k in mods}
    for st in all_stories:
        key = st.moderator
        if key in ps.keys() and not st.status:
            ps[key] += 1
    return render_template('Story/stories.html', stories=stories, mods=mods, ps=ps)


@story.route('/<story_id>')
def view(story_id):
    form = CommentForm()
    if story_id:
        story = Story.query.filter_by(id=story_id).first()
        cmts = Comment.query.filter_by(story=story.id).all()
        replies = [r.comment_id for r in Reply.query.all()]
        comments = [c for c in cmts if c.id not in replies]
        if story:
            return render_template('Story/view.html', story=story, form=form, comments=comments)
        return redirect(url_for('story.index'))
    return redirect(url_for('story.index'))


@story.route('/share', methods=('GET', 'POST', ))
def share():
    form = CreateStoryForm()
    if form.validate_on_submit():
        try:
            story = Story(
                form.title.data,
                form.content.data,
                form.allow_comments.data)
            db.session.add(story)
            db.session.commit()
        except IntegrityError:
            flash('Error saving!')
            return redirect(url_for('transgresion.share'), form=form)
        flash("Success! Thank you for sharing!")
        return redirect(url_for('story.index'))
    return render_template('Story/share.html', form=form)
