from data.__all_models import User, Post
from data.forms import NewPostForm
from flask_login import current_user
from flask import render_template
import flask
import datetime
import json

from data import db_session

blueprint = flask.Blueprint(
    'main_page', __name__,
    template_folder='templates',
    static_folder="static"
)


def __post(session, form, data=[]):
    if form.validate_on_submit():
        post = Post()
        post.datetime = datetime.datetime.now()
        post.author = current_user.id
        post.text = form.text.data.replace('<br>', '\n')
        post.q_and_a = 'q&a' in data
        post.anonymous = 'anon' in data
        session.add(post)
        session.commit()
        author = session.query(User).get(current_user.id)
        author.posts += f",{session.query(Post).filter(Post.author == current_user.id).all()[-1].id}"
        session.commit()


@blueprint.route('/account/<int:user_id>', methods=['GET', 'POST'])
def account(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    form = NewPostForm()
    data = {
        'user': user,
        'session': session,
        'posts': [session.query(Post).get(post_id) for post_id in user.posts.strip().split(",") if
                  post_id.strip() != ""],
        'form': form,
        'User': User,
        'len': len,
        'current_user': current_user
    }
    __post(session, form)
    return render_template("account.html", **data)


@blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    session = db_session.create_session()
    form = NewPostForm()
    data = {
        'session': session,
        'posts': session.query(Post).all(),
        'form': form,
        'User': User,
        'len': len,
        'current_user': current_user,
        'get_user': lambda x: session.query(User).get(x)
    }
    __post(session, form, flask.request.form.getlist('checkbox'))
    return render_template("home.html", **data)
