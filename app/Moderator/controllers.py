from functools import wraps

from flask import Blueprint, render_template, session, \
                  redirect, request, url_for, flash, g, abort
from flask_login import login_user, login_required, logout_user, \
                        current_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.Moderator.forms import LoginForm, CreateForm, EditForm
from app.Moderator.models import Moderator
from app.Story.models import Story


mods = Blueprint('mods', __name__, url_prefix='/private')


@mods.route('/login', methods=('GET', 'POST', ))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Moderator.query.filter_by(email=form.email.data).first()
        if user and user.validate(form.password.data):
            login_user(user)
            return redirect(url_for('mods.pending'))
        flash('Your email or password is incorrect!')
    return render_template('Moderator/login.html', form=form)



@mods.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!")
    return redirect(url_for('mods.login'))


@mods.route('/create', methods=('GET', 'POST', ))
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        try:
            mod = Moderator.create(
                form.name.data,
                form.email.data,
                form.password.data)
            db.session.add(mod)
            db.session.commit()
        except IntegrityError:
            flash('Moderator already exists!', 'error')
            return render_template('create.html', form=form)
        flash('Moderator created successfully!', 'success')
        return redirect(url_for('mods.pending'))
    return render_template('Moderator/create.html', form=form)


@mods.route('/pending')
@login_required
def pending():
    if current_user:
        pending_stories = Story.query.filter_by(status=False, moderator=current_user.id).all()
    else:
        pending_stories = []
    return render_template('Moderator/pending.html', pending_stories=pending_stories)


@mods.route('/pending/edit/<story_id>', methods=('GET', 'POST', ))
@login_required
def edit_story(story_id):
    story = Story.query.get(story_id)
    if current_user and current_user.is_authenticated:
        if not story or story.moderator != current_user.id:
            flash('You do not have permission to view this resource.')
            return redirect(url_for('mods.pending'))
        if story.status:
            flash('You cannot edit an approved story')
            return redirect(url_for('mods.pending'))
    else:
        flash('You do not have permission to view this resource.')
        return redirect(url_for('mods.login'))
    form = EditForm(obj=story)
    if form.validate_on_submit():
        try:
            story.title = form.title.data
            story.content = form.content.data
            story.status = form.status.data
            db.session.commit()
        except:
            print('Failure?')
        flash('Incident Approved')
        return redirect(url_for('mods.pending'))
    if not story_id:
        flash('You do not have permission to view this resource.')
        return redirect(url_for('mods.pending'))
    if not story:
        flash('No resource found by that ID: %d' % story_id)
        return redirect(url_for('mods.pending'))
    return render_template('Moderator/edit.html', story=story, form=form)

