from sqlalchemy import Column, Integer, Text, DateTime, String, Boolean, ForeignKey
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Event(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "events"
	id = Column(Integer, primary_key=True, autoincrement=True)
	datetime = Column(DateTime)
	text = Column(String)


class Message(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "messages"
	id = Column(Integer, primary_key=True, autoincrement=True)
	sender = Column(Integer)
	receiver = Column(Integer)
	text = Column(String)
	datetime = Column(DateTime)
	is_read = Column(Boolean, default=False)


class User(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String, unique=True)
	email = Column(String, unique=True)
	password = Column(String)
	description = Column(Text, default="")
	posts = Column(String, default="")
	likes = Column(String, default="")
	follows = Column(String, default="")


class Post(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "posts"
	id = Column(Integer, primary_key=True, autoincrement=True)
	author = Column(Integer, ForeignKey('users.id'))
	text = Column(Text)
	q_and_a = Column(Boolean)
	anonymous = Column(Boolean)
	datetime = Column(DateTime)
	comments = Column(String, default="")
	refers = Column(Integer, default=-1)
	likes = Column(String, default="")
	dislikes = Column(String, default="")
	ideas = Column(String, default="")


class Idea(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "ideas"
	id = Column(Integer, primary_key=True, autoincrement=True)
	posts = Column(String, default="")
	likes = Column(String, default="")
	dislikes = Column(String, default="")
	authors = Column(String)


class FilePost(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "files"
	id = Column(Integer, primary_key=True, autoincrement=True)
	way = Column(String)
	author = Column(Integer, ForeignKey('users.id'))
	post_id = Column(Integer, ForeignKey('posts.id'))
