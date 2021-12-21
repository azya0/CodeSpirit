from sqlalchemy import Column, Integer, Text, DateTime, String, Boolean, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Notification(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "notifications"
	id = Column(Integer, primary_key=True, autoincrement=True)
	author = Column(Integer, ForeignKey('users.id'))
	to_user = Column(Integer, ForeignKey('users.id'))
	datetime = Column(DateTime)
	watched = Column(Boolean, default=False)
	text = Column(String)
	link_to_watch = Column(String, nullable=False)
	type = Column(Integer, ForeignKey('notifications_type.id'))


class Notification_type(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "notifications_type"
	id = Column(Integer, primary_key=True, autoincrement=True)
	type = Column(String, nullable=False)


class Message(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "messages"
	id = Column(Integer, primary_key=True, autoincrement=True)
	sender_index = Column(Integer, ForeignKey('message_sender_index.id'))
	text = Column(String)
	datetime = Column(DateTime)
	is_read = Column(Boolean, default=False)


class MessageSenderIndex(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "message_sender_index"
	id = Column(Integer, primary_key=True, autoincrement=True)
	sender = Column(Integer)
	receiver = Column(Integer)


class User(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String)
	email = Column(String)
	password = Column(String)
	description = Column(Text, default="")
	avatar = Column(Integer, ForeignKey('avatars.id'), default=0)


class Avatar(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "avatars"
	id = Column(Integer, primary_key=True, autoincrement=True)
	way = Column(String, nullable=False)


class Post(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "posts"
	id = Column(Integer, primary_key=True, autoincrement=True)
	author = Column(Integer, ForeignKey('users.id'))
	text = Column(Text, default='')
	turn_off_comments = Column(Boolean, default=False)
	anonymous = Column(Boolean)
	datetime = Column(DateTime)


class QAA(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "qaa"
	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String)
	author = Column(Integer, ForeignKey('users.id'))
	text = Column(Text, default='')
	anonymous = Column(Boolean)
	datetime = Column(DateTime)
	tags = Column(String, default="")
	views = Column(Integer, default=0)


class Answer(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "answ"
	id = Column(Integer, primary_key=True, autoincrement=True)
	qaa_id = Column(Integer, ForeignKey('qaa.id'))
	author = Column(Integer, ForeignKey('users.id'))
	text = Column(Text, default='')
	datetime = Column(DateTime)
	right_answer = Column(Boolean, default=False)


class File(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "files"
	id = Column(Integer, primary_key=True, autoincrement=True)
	way = Column(String)
	type = Column(String)
	author = Column(Integer, ForeignKey('users.id'))
	post_id = Column(Integer, ForeignKey('posts.id'))


class Comment(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "comments"
	id = Column(Integer, primary_key=True, autoincrement=True)
	text = Column(String)
	author = Column(Integer, ForeignKey('users.id'))
	post_id = Column(Integer, ForeignKey('posts.id'))
	datetime = Column(DateTime)


class Like(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "likes"
	id = Column(Integer, primary_key=True, autoincrement=True)
	author = Column(Integer, ForeignKey('users.id'))
	obj_id = Column(Integer, ForeignKey('like_obj.id'))
	dislike = Column(Boolean, default=False)
	datetime = Column(DateTime)


class LikeObj(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "like_obj"
	id = Column(Integer, primary_key=True, autoincrement=True)
	type_id = Column(Integer, ForeignKey('type_obj.id'))
	obj_id = Column(Integer)


class TypeObj(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "type_obj"
	id = Column(Integer, primary_key=True, autoincrement=True)
	type = Column(String, unique=True)


class QaaComment(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "qaa-comments"
	id = Column(Integer, primary_key=True, autoincrement=True)
	text = Column(String)
	author = Column(Integer, ForeignKey('users.id'))
	answer_id = Column(Integer, ForeignKey('answ.id'))
	datetime = Column(DateTime)
