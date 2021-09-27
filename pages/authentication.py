from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from data.forms import LoginForm, RegistrationForm
from data.__all_models import User, Post, Idea
from flask import render_template, redirect
import flask
import json

from data import db_session

blueprint = flask.Blueprint(
    'authentication', __name__,
    template_folder='templates',
    static_folder="static"
)


@blueprint.route("/registration", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if session.query(User).filter(User.email == form.email.data).first() is not None:
            return render_template("registration.html", message="This email is already taken",
                                   current_user=current_user, form=form)
        if session.query(User).filter(User.name == form.name.data).first() is not None:
            return render_template("registration.html", message="This login is already taken",
                                   current_user=current_user, form=form)
        user = User()
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)
        user.name = form.name.data
        user.description = form.description.data
        session.add(user)
        session.commit()
        login_user(user)
        return redirect("/")
    return render_template("registration.html", message="", current_user=current_user, form=form)


@blueprint.route("/login", methods=["POST", "GET"])
def login():
    form, message = LoginForm(), ""
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.login.data).first()
        if user is None:
            message = "No user found"
        elif check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect("/")
        else:
            message = "Wrong password"
    return render_template("login.html", current_user=current_user, form=form, message=message)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
