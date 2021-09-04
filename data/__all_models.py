from sqlalchemy import Column, Integer, Text, DateTime, String
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class User(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String)
	email = Column(String)
	descritpion = Column(Text)
	posts = Column(String)
	likes = Column(String)
	follows = Column(String)


class Post(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "posts"
	id = Column(Integer, primary_key=True, autoincrement=True)
	author = Column(Integer)
	text = Column(Text)
	datetime = Column(DateTime)
	comments = Column(String)
	refers = Column(Integer)
	likes = Column(String)
	dislikes = Column(String)
	ideas = Column(String)


class Idea(UserMixin, SqlAlchemyBase, SerializerMixin):
	__tablename__ = "ideas"
	id = Column(Integer, primary_key=True, autoincrement=True)
	posts = Column(String)
	likes = Column(String)
	dislikes = Column(String)
	authors = Column(String)
