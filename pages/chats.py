from flask_login import login_required, current_user
from data.__all_models import User, Message
from flask import render_template, redirect
from data.request_tools import *
from data.forms import NewPostForm
import datetime
import flask

from data import db_session

blueprint = flask.Blueprint(
    'chats', __name__,
    template_folder='templates',
    static_folder="static"
)


@login_required
@blueprint.route("/inbox/")
def inbox():
    session = db_session.create_session()

    indexes = session.query(MessageSenderIndex).filter(MessageSenderIndex.receiver == current_user.id).all()
    users = tuple(set(session.query(User).get(index.sender) for index in indexes))
    viewer_data = {
        user: session.query(Message).filter(Message.sender_index == get_sender_index(user.id, current_user.id).id).all()[-1] for user in users
    }
    data = {}
    if current_user.is_authenticated:
        notifications, unwatched_notifications = get_notification()
        data['notifications'] = list(notifications)[::-1]
        data['unwatched'] = unwatched_notifications
        data['get_user'] = get_user
    return render_template("messages.html", viewer_data=viewer_data, **data)


@login_required
@blueprint.route("/inbox/im/<int:id>", methods=['GET', 'POST'])
def im(id):
    from data.forms import MessageForm
    form = MessageForm()
    if form.validate_on_submit():
        from pages.home import format_string
        session = db_session.create_session()
        msg = Message()
        sender_index = get_sender_index(current_user.id, id)
        if sender_index == -1:
            sender_index = MessageSenderIndex()
            sender_index.sender = current_user.id
            sender_index.receiver = id
            session.add(sender_index)
            session.commit()
        msg.sender_index = sender_index.id
        msg.text = format_string(form.text.data)
        msg.datetime = datetime.datetime.now()
        session.add(msg)
        session.commit()
        return redirect(f"/inbox/im/{id}")
    session = db_session.create_session()
    try:
        sender_messages = session.query(Message).filter(
            Message.sender_index == get_sender_index(id, current_user.id).id).all()
    except AttributeError:
        sender_messages = []
    try:
        receiver_messages = session.query(Message).filter(
            Message.sender_index == get_sender_index(current_user.id, id).id).all()
    except AttributeError:
        receiver_messages = []
    _messages = sorted(list(set(sender_messages + receiver_messages)), key=lambda x: x.datetime)
    data = {
        'messages': _messages,
        'current_user': current_user,
        'get_message_author': get_message_author,
        'enumerate': enumerate,
        'form': form,
    }
    if current_user.is_authenticated:
        notifications, unwatched_notifications = get_notification()
        data['notifications'] = list(notifications)[::-1]
        data['unwatched'] = unwatched_notifications
        data['get_user'] = get_user
    return render_template("im.html", **data)
