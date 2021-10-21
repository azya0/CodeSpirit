from werkzeug.utils import secure_filename
from data.__all_models import User, Post, FilePost, Comment
from data.forms import NewPostForm, CommentForm
from flask_login import current_user
from flask import render_template
import flask
import datetime
import json
import os

from data import db_session

blueprint = flask.Blueprint(
    'main_page', __name__,
    template_folder='templates',
    static_folder="static"
)


def format_string(string: str) -> str:
    replace_dict = {
        '&nbsp;': ' ',
        '<div>': '',
        '</div>': '',
        '<br>': '\n'
    }
    string = string.strip()
    for elm in replace_dict:
        string = string.replace(elm, replace_dict[elm]).strip()
    return string


def update_last_folder(last_file_way):
    import configparser
    config = configparser.ConfigParser()
    config.read('static/config.ini')
    config['App']['last_file_way'] = last_file_way
    with open('static/config.ini', 'w') as configfile:
        config.write(configfile)


def add_file():
    def last_section(data, num):
        if len(set(data[:-1])) == 1 and data[0] == 'z':
            for i in range(len(data) - 1):
                data[i] = 'a'
            data.insert(-1, 'a')
            return data
        letter = data[-num]
        if letter == 'z':
            del data[-num]
            return last_section(data, num)
        else:
            data[-num] = chr(ord(letter) + 1)
        return data

    last_data = flask.current_app.config['last_uploaded_file'].split('/')
    last_data[-1] = str((int(last_data[-1]) + 1) % 10)
    if not int(last_data[-1]):
        last_data = last_section(last_data, 2)
    under_return = '/'.join(last_data)
    return under_return[:-1], under_return[-1]


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
    return render_template("account.html", **data)


@blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    session = db_session.create_session()
    form = NewPostForm()
    comment_form = CommentForm()
    data = {
        'session': session,
        'posts': session.query(Post).all(),
        'files': session.query(FilePost),
        'comments': session.query(Comment),
        'form': form,
        'comment_form': comment_form,
        'User': User,
        'FilePost': FilePost,
        'Comment': Comment,
        'current_user': current_user,
        'len': len,
        'str': str,
        'enu': enumerate,
        'string_long': lambda x: 1 if len(x) >= 400 else 2 if x.count('\n') > 14 else 0,
        'string_long_p': lambda x: 1 if len(x) >= 4000 else 2 if x.count('\n') > 14 else 0,
        'is_file': lambda x: os.path.exists(x),
        'get_user': lambda x: session.query(User).get(x)
    }
    return render_template("home.html", **data)


@blueprint.route('/add_post', methods=['POST'])
def add_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post, data, session = Post(), flask.request.form.getlist('checkbox'), db_session.create_session()
        post.datetime = datetime.datetime.now()
        post.author = current_user.id
        print(form.text)
        post.text = format_string(form.text.data)
        if not post.text:
            return flask.redirect('/')
        post.q_and_a = 'q&a' in data
        post.anonymous = 'anon' in data
        f_req = flask.request.files.getlist("image_input[]")

        files = []
        for file in f_req:
            if not file.filename:
                continue
            file_way, filename = add_file()
            flask.current_app.config['last_uploaded_file'] = file_way + filename
            update_last_folder(file_way + filename)
            for i in range(len(file_way[:-1])):
                try:
                    os.mkdir(flask.current_app.config['UPLOAD_FOLDER'] + '/' + '/'.join(file_way[:-1][:i + 1]))
                except FileExistsError:
                    pass

            file.save(os.path.join(f"{flask.current_app.config['UPLOAD_FOLDER']}/{file_way[:-1]}",
                                   filename + '.' + file.filename.split('.')[-1]))
            files += [f"{flask.current_app.config['UPLOAD_FOLDER']}/{file_way}" + filename + '.' + file.filename.split('.')[-1]]

        if not post.text and not files:
            return False

        session.add(post)
        for way in files:
            file = FilePost()
            file.author = current_user.id
            file.post_id = session.query(Post).filter(Post.author == current_user.id).all()[-1].id
            file.way = way
            session.add(file)
        author = session.query(User).get(current_user.id)
        author.posts += f",{session.query(Post).filter(Post.author == current_user.id).all()[-1].id}"
        session.commit()
    return flask.redirect('/')


@blueprint.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id: int):
    form = CommentForm()
    if form.validate_on_submit():
        comment, session = Comment(), db_session.create_session()
        comment.text = format_string(form.text.data)
        if not comment.text:
            return flask.redirect('/')
        comment.author = current_user.id
        comment.post_id = post_id
        comment.datetime = datetime.datetime.now()
        session.add(comment)
        session.commit()
    return flask.redirect('/')
