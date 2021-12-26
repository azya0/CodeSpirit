from werkzeug.utils import secure_filename
from data.__all_models import *
from data.forms import *
from flask_login import login_required, current_user
from data.request_tools import *
from flask import render_template
import flask
import datetime
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
        '\\n': '\n'
    }

    string = string.strip()
    for elm in replace_dict:
        string = string.replace(elm, replace_dict[elm]).strip()
    return string.strip()


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


@blueprint.route('/profile', methods=['GET', 'POST'])
def self_account():
    return account(current_user.id)


@login_required
@blueprint.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def account(user_id):
    from pages.q_and_a import mini_qaa_text
    from random import randint

    session = db_session.create_session()
    user = session.query(User).get(user_id)
    form = NewPostForm()
    all_user_activity = dict()
    for elm in session.query(Post).filter(Post.author == user_id).all():
        all_user_activity[elm] = 'post'
    for elm in session.query(QAA).filter(QAA.author == user_id).all():
        all_user_activity[elm] = 'qaa'
    comment_form = CommentForm()
    data = {
        'user': user,
        'session': session,
        'posts': session.query(Post).filter(Post.author == user_id).all(),
        'get_user_avatar': get_user_avatar,
        'sorted_data': sorted(all_user_activity, key=lambda x: x.datetime, reverse=True),
        'all_user_data_type': all_user_activity,
        'files': session.query(File),
        'answers': session.query(Answer),
        'likes': session.query(Like),
        'questions': sorted(session.query(QAA).all(), key=lambda x: x.datetime, reverse=True),
        'form': form,
        'User': User,
        'File': File,
        'Like': Like,
        'current_user': current_user,
        'question_rating': get_QaaPost_rating,
        'gradient': lambda: f'linear-gradient({randint(40, 160)}deg, rgba({randint(80, 255)},50,{randint(56, 110)},1)'
                            f'0%, rgba({randint(15, 100)},{randint(0, 107)},{randint(170, 250)},1) 28%,'
                            f'rgba({randint(151, 200)},{randint(50, 140)},{randint(10, 56)},1) 72%);',
        'enumerate': enumerate,
        'qaa_text': mini_qaa_text,
        'author': lambda x: session.query(User).get(x),
        'answ_count': lambda x: len(session.query(Answer).filter(Answer.qaa_id == x).all()),
        'answered': lambda x: session.query(Answer).filter(Answer.qaa_id == x).filter(
            Answer.right_answer == True).first(),
        'comments': session.query(Comment),
        'comment_form': comment_form,
        'Comment': Comment,
        'sorted': sorted,
        'cl_filter': lambda x: get_CommentLike_count(x.id),
        'len': len,
        'str': str,
        'enu': enumerate,
        'string_long': lambda x: 1 if len(x) >= 400 else 2 if x.count('\n') > 14 else 0,
        'string_long_p': lambda x: 1 if len(x) >= 1700 else 2 if x.count('\n') > 14 else 0,
        'is_liked': is_liked,
        'get_CommentLike_count': get_CommentLike_count,
        'is_file': lambda x: os.path.exists(x),
        'get_user': lambda x: session.query(User).get(x)
    }
    notifications, unwatched_notifications = get_notification()
    data['notifications'] = list(notifications)[::-1]
    data['unwatched'] = unwatched_notifications
    data['get_user'] = get_user
    data['unwatched_msgs'] = get_unwroten_messages_count(current_user.id)
    data['get_user_avatar'] = get_user_avatar
    return render_template("profile.html", **data)


@login_required
@blueprint.route('/upload_avatar', methods=['GET', 'POST'])
def upload_avatar():
    def get_filename(_filename):
        last_server_num = sorted(map(lambda x: int(x.split('.')[0]), os.listdir('static/avatars')))[-1] + 1
        return f'{last_server_num}.' + _filename.split('.')[-1]

    def crop_center(pil_img, crop_width: int, crop_height: int):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))

    file = flask.request.files['avatar-input']
    if file:
        filename = get_filename(file.filename)
        file.save(os.path.join(flask.current_app.config['AVATAR_FOLDER'], filename))
        full_fileway = flask.current_app.config['AVATAR_FOLDER'] + '/' + filename
        from PIL import Image

        im = Image.open(full_fileway)
        im_new = crop_center(im, 460, 460)
        im_new.save(full_fileway, quality=95)

        session = db_session.create_session()

        user = session.query(User).get(current_user.id)
        if user.avatar:
            avatar = session.query(Avatar).get(user.avatar)
            os.remove(avatar.way)
            session.delete(avatar)

        avatar = Avatar()
        avatar.way = full_fileway
        session.add(avatar)
        session.commit()
        user.avatar = avatar.id
        session.commit()
    return self_account()


def is_liked(id):
    session = db_session.create_session()
    data = session.query(Like).filter(Like.author == current_user.id).filter(
        Like.obj_id == get_LikeObj_id(id, 'Comment')).first()
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
        'cl_filter': lambda x: get_CommentLike_count(x.id),
        'len': len,
        'str': str,
        'enu': enumerate,
        'string_long': lambda x: 1 if len(x) >= 400 else 2 if x.count('\n') > 14 else 0,
        'string_long_p': lambda x: 1 if len(x) >= 1700 else 2 if x.count('\n') > 14 else 0,
        'is_liked': is_liked,
        'get_CommentLike_count': get_CommentLike_count,
        'is_file': lambda x: os.path.exists(x),
        'get_user': lambda x: session.query(User).get(x),
        'get_user_avatar': get_user_avatar
    }
    if current_user.is_authenticated:
        notifications, unwatched_notifications = get_notification()
        data['notifications'] = list(notifications)[::-1]
        data['unwatched'] = unwatched_notifications
        data['unwatched_msgs'] = get_unwroten_messages_count(current_user.id)
        data['get_user_avatar'] = get_user_avatar
    return render_template("home.html", **data)


@blueprint.route('/add_post', methods=['POST'])
@login_required
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
        if not post.text and not flask.request.files.getlist("image_input[]"):
            return flask.redirect('/')
        post.turn_off_comments = 'toc' in data
        post.anonymous = 'anon' in data
        session.add(post)
        session.commit()
        files = get_files(flask.request.files.getlist("image_input[]"))
        add_img(files)
        session.commit()
    return flask.redirect('/')


@blueprint.route('/delete_post/<int:id>', methods=['DELETE'])
@login_required
def delete_post(id):
    session = db_session.create_session()
    post = session.query(Post).get(id)
    if post and current_user.id == post.author:
        session.delete(post)
    for file in session.query(File).filter(File.post_id == id).all():
        if os.path.isfile(file.way):
            os.remove(file.way)
        session.delete(file)
    for comment in session.query(Comment).filter(Comment.post_id == id).all():
        delete_comment(comment.id)
    session.commit()
    return flask.jsonify({'success': True})


@blueprint.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
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
            post = session.query(Post).get(post_id)
            fileway = flask.url_for('static', filename=get_user_avatar(current_user.id))
            avatar = f"<img class='main-user-avatar-img-c' src='{fileway}'>" \
                if get_user(current_user.id).avatar \
                else '<i class="fa fa-user-circle main-comment-a-ava main-white-font-color i-c" aria-hidden="true"></i>'
            create_notification(current_user.id,
                                post.author,
                                f'{get_user_name(current_user.id)} comment your post: "{post.text[:10]}..."',
                                f'/', 'comment')
            return flask.jsonify({'result': 'success',
                                  'id': comment.id,
                                  'author': session.query(User).get(comment.author).name,
                                  'text': comment.text,
                                  'datetime': comment.datetime,
                                  'avatar': avatar,
                                  'is_first': True if len(session.query(Comment).filter(
                                      Comment.post_id == post_id).all()) == 1 else False})
    except BaseException as exception:
        return flask.jsonify({'result': 'error', 'error': f'{exception}'})
    return flask.jsonify({'result': 'unvalidated'})


@blueprint.route('/like/<string:type_>/<int:id>', methods=['GET', 'PUT'])
@login_required
def is_comment_liked(type_: str, id: int):
    session = db_session.create_session()
    _type = get_TypeObj_id(type_)
    if _type == -1:
        return flask.jsonify({'result': 'Wrong object type'})
    like_obj = session.query(LikeObj).filter(LikeObj.type_id == _type).filter(LikeObj.obj_id == id).first()
    if not like_obj:
        like_obj = LikeObj()
        like_obj.obj_id = id
        like_obj.type_id = _type
        session.add(like_obj)
        session.commit()
    like = session.query(Like).filter(Like.obj_id == like_obj.id).filter(Like.author == current_user.id).first()
    if like:
        session.delete(like)
        session.commit()
        obj = session.query(get_class(get_TypeObj(like_obj.type_id).type)).get(like_obj.obj_id)
        notification = session.query(Notification).filter(
            Notification.author == current_user.id).filter(
            Notification.to_user == obj.author).filter(
            Notification.link_to_watch == f'/').filter(
            Notification.type == get_Notification_type_id('like')).first()
        if notification:
            session.delete(notification)
            session.commit()
        return flask.jsonify({'result': 'cancel'})
    else:
        like = Like()
        like.author = current_user.id
        like.obj_id = like_obj.id
        like.datetime = datetime.datetime.now()
        session.add(like)
        obj = session.query(get_class(get_TypeObj(like_obj.type_id).type)).get(like_obj.obj_id)
        session.commit()
        create_notification(current_user.id,
                            obj.author,
                            f'{get_user_name(current_user.id)} like your {get_TypeObj(like_obj.type_id).type.lower()}',
                            f'/', 'like')
    return flask.jsonify({'result': 'add'})


@blueprint.route('/delete_comment/<int:id>', methods=['DELETE'])
@login_required
def delete_comment(id):
    session = db_session.create_session()
    comment = session.query(Comment).get(id)
    if comment and current_user.id == comment.author:
        session.delete(comment)
    for like in session.query(Like).filter(Like.obj_id == get_LikeObj_id(id, 'Comment')).all():
        session.delete(like)
    session.commit()
    post = session.query(Post).get(comment.post_id)
    notification = session.query(Notification).filter(
        Notification.author == current_user.id).filter(
        Notification.to_user == post.author).filter(
        Notification.link_to_watch == f'/').filter(
        Notification.type == get_Notification_type_id('comment')).first()
    if notification:
        session.delete(notification)
        session.commit()
    return flask.jsonify({'success': True})


@login_required
@blueprint.route('/announce/<int:id>', methods=['GET'])
def announce(id):
    session = db_session.create_session()
    notification = session.query(Notification).get(id)

    if not notification.watched:
        notification.watched = True
        session.commit()
    return flask.redirect(notification.link_to_watch)
