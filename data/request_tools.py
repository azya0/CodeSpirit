from data import db_session
from data.__all_models import *


def get_TypeObj_id(_type):
    session = db_session.create_session()
    obj = session.query(TypeObj).filter(TypeObj.type == _type).first()
    return obj.id if obj else -1


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
