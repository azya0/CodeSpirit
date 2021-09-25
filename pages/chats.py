from flask_login import login_required, current_user
from data.__all_models import User, Message
from flask import render_template, redirect
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
@blueprint.route("/messages/<int:user_id>", methods=['GET', 'POST'])
def messages(user_id: int):
    session = db_session.create_session()
    messages = session.query(Message).filter(Message.receiver == current_user.id and Message.sender == user_id or Message.receiver == user_id and Message.sender == current_user.id).all()
    messages = messages[-5:]
    pair = {current_user.id: session.query(User).get(current_user.id).name, user_id: session.query(User).get(user_id).name}
    form = NewPostForm()
    if form.validate_on_submit():
        new_message = Message()
        new_message.sender = current_user.id
        new_message.receiver = user_id
        new_message.text = form.text.data
        new_message.datetime = datetime.datetime.now()
        session.add(new_message)
        session.commit()
        return redirect(f"/messages/{user_id}")
    return render_template("chat.html", messages=messages, pair=pair, form=form)


@login_required
@blueprint.route("/inbox/")
def inbox():
    session = db_session.create_session()
    all_messages = session.query(Message).filter(Message.receiver ==
        current_user.id or Message.sender == current_user.id).all()
    sorted_messages = dict()
    for message in all_messages:
        if message.receiver == current_user.id:
            sorted_messages[message.sender] = message
        else:
            sorted_messages[message.receiver] = message
    sorted_messages = [(session.query(User).get(id).name, sorted_messages[id].datetime, sorted_messages[id].text[:10], id) for id in sorted_messages.keys()]
    sorted_messages.sort(key=lambda x: x[1], reverse=True)
    return render_template("messages.html", messages=sorted_messages)
