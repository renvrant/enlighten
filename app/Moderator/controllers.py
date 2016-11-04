from functools import wraps

from flask import Blueprint, render_template, session, \
                  redirect, request, url_for, flash, g, abort
from flask_login import login_user, login_required, logout_user, \
                        current_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.Moderator.forms import LoginForm, CreateForm, EditForm
from app.Moderator.models import Moderator
from app.Transgression.models import Transgression


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
        pending_tgs = Transgression.query.filter_by(status=False, moderator=current_user.id).all()
    else:
        pending_tgs = []
    return render_template('Moderator/pending.html', pending_transgressions=pending_tgs)


@mods.route('/pending/edit/<tg_id>', methods=('GET', 'POST', ))
@login_required
def edit_tg(tg_id):
    tg = Transgression.query.get(tg_id)
    form = EditForm(obj=tg)
    if form.validate_on_submit():
        try:
            tg.title = form.title.data
            tg.content = form.content.data
            tg.status = form.status.data
            db.session.commit()
        except:
            print('Failure?')
        return redirect(url_for('mods.pending'))
    if not tg_id:
        return redirect(url_for('mods.pending'))
    tg = Transgression.query.filter_by(id=tg_id).first()
    if not tg:
        return redirect(url_for('mods.pending'))
    return render_template('Moderator/edit.html', tg=tg, form=form)

