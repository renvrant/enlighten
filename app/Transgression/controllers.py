from flask import render_template, redirect, url_for, abort, Blueprint, \
                  flash
from flask_login import login_required, logout_user, login_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.Transgression.forms import CreateTransgressionForm
from app.Transgression.models import Transgression


transgression = Blueprint('transgression', __name__, url_prefix='/common')


@transgression.route('/')
def index():
    transgressions = Transgression.query.filter_by(status=True)
    return render_template('Transgression/transgressions.html', transgressions=transgressions)


@transgression.route('/<transgression_id>')
def view(transgression_id):
    if transgression_id:
        transgression = Transgression.query.filter_by(id=transgression_id).first()
        if transgression:
            return render_template('Transgression/view.html', transgression=transgression)
        return redirect(url_for('transgression.index'))
    return redirect(url_for('transgression.index'))


@transgression.route('/share', methods=('GET', 'POST', ))
def share():
    form = CreateTransgressionForm()
    if form.validate_on_submit():
        try:
            tg = Transgression(form.title.data, form.content.data)
            db.session.add(tg)
            db.session.commit()
        except IntegrityError:
            flash('Error saving!')
            return redirect(url_for('transgresion.share'), form=form)
        flash("Success! Thank you for sharing!")
        return redirect(url_for('transgression.index'))
    return render_template('Transgression/share.html', form=form)
