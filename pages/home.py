from werkzeug.utils import secure_filename
from data.__all_models import *
from data.forms import NewPostForm, CommentForm
from flask_login import login_required, current_user
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
        '\\n': '\n'
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


def is_liked(id):
    session = db_session.create_session()
    data = session.query(Like).filter(Like.author == current_user.id).filter(
        Like.type == 'comment').filter(Like.obj_id == id).first()
    return data


@blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    session = db_session.create_session()
    form = NewPostForm()
    comment_form = CommentForm()
    data = {
        'session': session,
        'posts': sorted(session.query(Post).all(), key=lambda x: x.datetime, reverse=True),
        'files': session.query(File),
        'comments': session.query(Comment),
        'likes': session.query(Like),
        'form': form,
        'comment_form': comment_form,
        'User': User,
        'File': File,
        'Like': Like,
        'Comment': Comment,
        'current_user': current_user,
        'sorted': sorted,
        'cl_filter': lambda x: x.likes,
        'len': len,
        'str': str,
        'enu': enumerate,
        'string_long': lambda x: 1 if len(x) >= 400 else 2 if x.count('\n') > 14 else 0,
        'string_long_p': lambda x: 1 if len(x) >= 1700 else 2 if x.count('\n') > 14 else 0,
        'is_liked': is_liked,
        'is_file': lambda x: os.path.exists(x),
        'get_user': lambda x: session.query(User).get(x)
    }
    return render_template("home.html", **data)


@login_required
@blueprint.route('/add_post', methods=['POST'])
def add_post():
    def get_files(f_req):
        file_list = []
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
            file_list += [
                f"{flask.current_app.config['UPLOAD_FOLDER']}/{file_way}" + filename + '.' + file.filename.split('.')[
                    -1]]
        return file_list

    def add_img(file_list):
        if not post.text and not file_list:
            return

        for way in file_list:
            file = File()
            file.type = 'img'
            file.author = current_user.id
            file.post_id = session.query(Post).filter(Post.author == current_user.id).all()[-1].id
            file.way = way
            session.add(file)

    form = NewPostForm()
    if form.validate_on_submit():
        post, data, session = Post(), flask.request.form.getlist('checkbox'), db_session.create_session()
        post.datetime = datetime.datetime.now()
        post.author = current_user.id
        post.text = format_string(form.text.data)
        if not post.text:
            return flask.redirect('/')
        post.q_and_a = 'q&a' in data
        post.anonymous = 'anon' in data
        session.add(post)
        files = get_files(flask.request.files.getlist("image_input[]"))
        add_img(files)
        session.commit()
    return flask.redirect('/')


@login_required
@blueprint.route('/delete_post/<int:id>', methods=['DELETE'])
def delete_post(id):
    session = db_session.create_session()
    post = session.query(Post).get(id)
    if post and current_user.id == post.author:
        session.delete(post)
        session.commit()
    return flask.jsonify({'success': True})


@login_required
@blueprint.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id: int):
    try:
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
            return flask.jsonify({'result': 'success',
                                  'id': comment.id,
                                  'author': session.query(User).get(comment.author).name,
                                  'text': comment.text,
                                  'datetime': comment.datetime,
                                  'is_first': True if len(session.query(Comment).filter(
                                      Comment.post_id == post_id).all()) == 1 else False})
    except BaseException as exception:
        return flask.jsonify({'result': 'error', 'error': f'{exception}'})
    return flask.jsonify({'result': 'unvalidated'})


@login_required
@blueprint.route('/like/<string:type_>/<int:id>', methods=['GET', 'PUT'])
def is_comment_liked(type_: str, id: int):
    WT_ERROR = flask.jsonify({'result': 'error: wrong type'})

    def correct_like(add):
        if type_ == 'post':
            obj = session.query(Post).filter(Post.id == id).first()
        else:
            obj = session.query(Comment).filter(Comment.id == id).first()
        obj.likes += 1 if add else -1

    def valid_type(type_of):
        return type_of in ('post', 'comment')

    if not valid_type(type_):
        return WT_ERROR

    session = db_session.create_session()
    like = session.query(Like).filter(Like.author == current_user.id).filter(
        Like.type == 'comment').filter(Like.obj_id == id).first()
    if like:
        if valid_type(like.type):
            correct_like(False)
        else:
            return WT_ERROR
        session.delete(like)
        result = 'cancel'
    else:
        new_like = Like()
        new_like.author = current_user.id
        new_like.obj_id = id
        new_like.type = type_
        session.add(new_like)
        correct_like(True)
        result = 'add'
    session.commit()
    return flask.jsonify({'result': result})


@login_required
@blueprint.route('/delete_comment/<int:id>', methods=['DELETE'])
def delete_comment(id):
    session = db_session.create_session()
    comment = session.query(Comment).get(id)
    if comment and current_user.id == comment.author:
        session.delete(comment)
    for like in session.query(Like).filter(Like.type == 'comment').filter(Like.obj_id == id).all():
        session.delete(like)
    session.commit()
    return flask.jsonify({'success': True})
