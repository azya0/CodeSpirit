from flask_login import current_user
from flask import render_template
import flask
import json

from data import db_session

blueprint = flask.Blueprint(
    'main_page', __name__,
    template_folder='templates',
    static_folder="static"
)


@blueprint.route('/')
def main_page():
    return render_template("main_page.html", current_user=current_user)
