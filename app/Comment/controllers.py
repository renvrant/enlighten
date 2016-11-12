from flask import Blueprint, render_template, session, \
                  redirect, request, url_for, flash, g, abort
from flask_login import login_user, login_required, logout_user, \
                        current_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.Comment.models import Comment, Reply
from app.Comment.forms import CommentForm
from app.Story.models import Story


comment = Blueprint('comment', __name__, url_prefix='/comment')


@comment.route('/new/<story_id>', methods=('POST', ))
@comment.route('/new/<story_id>/<comment_id>', methods=('POST', ))
def new(story_id, comment_id=None):
    if not story_id:
        flash('There was an error processing your request')
        return redirect(url_for('story.index'))
    form = CommentForm()
    if form.validate_on_submit():
        if current_user and current_user.is_authenticated:
            is_mod = True
        else:
            is_mod = False
        try:
            comment = Comment(
                form.title.data,
                form.body.data,
                is_mod,
                story_id)
            db.session.add(comment)
            db.session.commit()
        except:
            flash('There was an error processing your request')
            return redirect(request.referrer)
        if comment_id:
            reply = Reply(
                comment.id,
                comment_id)
            try:
                db.session.add(reply)
                db.session.commit()
            except:
                flash('There was an error processing your request')
                return redirect(request.referrer)
    flash('Comment added successfully!')
    return redirect(request.referrer)
