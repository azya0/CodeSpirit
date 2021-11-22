from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, Length
from data.validators import *


class NewPostForm(FlaskForm):
    __form__ = 'post'
    text = StringField("Enter the text")
    submit = SubmitField("Post")


class RegistrationForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired(), WhiteSpaceBanned(), Login()])
    email = StringField("E-mail", validators=[DataRequired(), Email('Incorrect email')])
    password = PasswordField("Password", validators=[DataRequired(), WhiteSpaceBanned()])
    confirm_password = PasswordField("Confirm password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match")])
    description = TextAreaField("Short description (you can fill it later)")
    submit = SubmitField("Let's go!")


class LoginForm(FlaskForm):
    login = StringField("Login (e-mail)", validators=[DataRequired(), WhiteSpaceBanned()])
    password = PasswordField("Password", validators=[DataRequired(), WhiteSpaceBanned()])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Let's go!")


class CommentForm(FlaskForm):
    __form__ = 'comment'
    text = StringField("write a comment...", validators=[DataRequired()])


class QAAForm(FlaskForm):
    __form__ = 'qaa'
    title = StringField('What is the problem? Be short', validators=[DataRequired(), SelfLength('title', min_length=5,
                                                                                                max_length=100)])
    text = TextAreaField(validators=[DataRequired(), SelfLength('text', min_length=50)])
    tags = StringField(validators=[Tag()])
    submit = SubmitField("Post")


class AnswerForm(FlaskForm):
    __form__ = 'qaa_answer'
    text = TextAreaField(validators=[DataRequired(), SelfLength('text', min_length=25)])
    submit = SubmitField("Answer")


class QaaCommentForm(FlaskForm):
    __form__  = 'qaa_comment'
    text = StringField(validators=[DataRequired(), SelfLength('text', max_length=250)])
    submit = SubmitField("Comment")
