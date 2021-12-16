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
