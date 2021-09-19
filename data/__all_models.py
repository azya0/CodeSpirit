from sqlalchemy import Column, Integer, Text, DateTime, String
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String)
	email = Column(String)
	password = Column(String)
	description = Column(Text, default="")
	posts = Column(String, default="")
	likes = Column(String, default="")
	follows = Column(String, default="")


class Post(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "posts"
	id = Column(Integer, primary_key=True, autoincrement=True)
	author = Column(Integer)
	text = Column(Text)
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
