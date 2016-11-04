from flask import render_template, redirect, url_for, abort, Blueprint, \
                  flash
from flask_login import login_required, logout_user, login_user
from sqlalchemy.exc import IntegrityError

from app import db
from app.Transgression.forms import CreateTransgressionForm
from app.Transgression.models import Transgression
from app.Moderator.models import Moderator


transgression = Blueprint('transgression', __name__, url_prefix='/common')


@transgression.route('/')
def index():
    tgs = Transgression.query.filter_by(status=True)

    # Uncomment this code to see which mods have pending from the index screen
    # for development only
    #
    # tgs = Transgression.query.all()
    # mods = [mod for mod in Moderator.query.all()]
    # ptgs = {k.id: 0 for k in mods}
    # for t in tgs:
    #     key = t.moderator
    #     if key in ptgs.keys():
    #         ptgs[key] += 1
    return render_template('Transgression/transgressions.html', tgs=tgs)  # , mods=mods, ptgs=ptgs)


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
