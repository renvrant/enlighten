from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_assets import Environment, Bundle


app = Flask(__name__)
app.config.from_object('config')

# Setup SCSS transpilation
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('main.scss', filters='pyscss', output='style.css')
assets.register('scss_all', scss)

# Init database and flask login
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Grab blueprints and necessary models
from app.Moderator.controllers import mods as mods_bp
from app.Moderator.models import Moderator as Mod
from app.Story.controllers import story as story_bp


# Register blueprints with main app
app.register_blueprint(mods_bp)
app.register_blueprint(story_bp)


@login_manager.user_loader
def load_user(mod_id):
    return Mod.query.filter_by(id=mod_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access that page')
    return redirect(url_for('mods.login'))


@app.route('/')
def index():
    return redirect(url_for('story.index'))


# Create the database
db.create_all();
