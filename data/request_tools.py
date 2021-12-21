from data import db_session
from data.__all_models import *
from flask_login import current_user


def get_TypeObj_id(_type):
    session = db_session.create_session()
    obj = session.query(TypeObj).filter(TypeObj.type == _type).first()
    return obj.id if obj else -1


def get_TypeObj(id):
    session = db_session.create_session()
    obj = session.query(TypeObj).get(id)
    return obj


def get_class(class_name):
    import data.__all_models

    for item in data.__all_models.__dict__.values():
        if isinstance(item, type):
            if class_name == item.__name__:
                return item
    return -1


def get_LikeObj(id, _type):
    session = db_session.create_session()
    obj = session.query(LikeObj).filter(LikeObj.obj_id == id).filter(LikeObj.type_id == get_TypeObj_id(_type)).first()
    return obj


def get_LikeObj_id(id, _type):
    session = db_session.create_session()
    obj = session.query(LikeObj).filter(LikeObj.obj_id == id).filter(LikeObj.type_id == get_TypeObj_id(_type)).first()
    return obj.id if obj else -1


def get_CommentLike_count(id):
    session = db_session.create_session()
    return len(session.query(Like).filter(Like.obj_id == get_LikeObj_id(id, 'Comment')).all())


def get_QaaPost_rating(id):
    session = db_session.create_session()
    return len(
        session.query(Like).filter(Like.obj_id == get_LikeObj_id(id, 'QAA')).filter(Like.dislike == False).all()) - \
        len(session.query(Like).filter(Like.obj_id == get_LikeObj_id(id, 'QAA')).filter(Like.dislike == True).all())


def get_Answer_rating(id):
    session = db_session.create_session()
    return len(
        session.query(Like).filter(
            Like.obj_id == get_LikeObj_id(id, 'Answer')).filter(Like.dislike == False).all()) - \
        len(session.query(Like).filter(
            Like.obj_id == get_LikeObj_id(id, 'Answer')).filter(Like.dislike == True).all())


def get_notification():
    session = db_session.create_session()
    notifications = session.query(Notification).filter(Notification.to_user == current_user.id)
    return notifications.all(), len(notifications.filter(Notification.watched == False).all())


def get_Notification_type(id):
    session = db_session.create_session()
    return session.query(Notification_type).get(id).type


def get_Notification_type_id(name):
    session = db_session.create_session()
    obj = session.query(Notification_type).filter(Notification_type.type == name).first()
    return obj.id if obj else -1


def create_notification(author, to_user, text, link_to_watch, type_):
    if True: # not current_user.id == author:
        import datetime
        session = db_session.create_session()
        notification = Notification()
        notification.author = author
        notification.to_user = to_user
        notification.datetime = datetime.datetime.now()
        notification.text = text
        notification.link_to_watch = link_to_watch
        notification.type = get_Notification_type_id(type_)
        session.add(notification)
        session.commit()


def get_user(id):
    session = db_session.create_session()
    return session.query(User).get(id)


def get_user_name(id):
    return get_user(id).name


def get_message_user_data(id):
    session = db_session.create_session()
    return session.query(MessageSenderIndex).get(id)


def get_message_author(index_id):
    session = db_session.create_session()
    return session.query(User).get(session.query(MessageSenderIndex).get(index_id).sender)


def get_sender_index(sender, receiver):
    session = db_session.create_session()
    result = session.query(MessageSenderIndex).filter(MessageSenderIndex.sender == sender)\
        .filter(MessageSenderIndex.receiver == receiver).first()
    return result if result else -1


def get_receiver_index(sender, receiver):
    session = db_session.create_session()
    result = session.query(MessageSenderIndex).filter(MessageSenderIndex.sender == sender)\
        .filter(MessageSenderIndex.receiver == receiver).first()
    return result if result else -1


def get_unwroten_messages_count(user_id):
    session = db_session.create_session()
    indexes = session.query(MessageSenderIndex).filter(MessageSenderIndex.receiver == user_id).all()
    return sum([0 if session.query(Message).filter(Message.sender_index == index.id)[-1].is_read
                else 1 for index in indexes])


def get_user_avatar(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    avatar = session.query(Avatar).get(user.avatar)
    return avatar.way[7:] if avatar else 0
