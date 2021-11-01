from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email


class NewPostForm(FlaskForm):
    __form__ = 'post'
    text = StringField("Enter the text")
    submit = SubmitField("Post")


class RegistrationForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email('Incorrect email')])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm password", validators=[
        DataRequired(), EqualTo("password", message="Passwords must match")])
    description = TextAreaField("Short description (you can fill it later)")
    submit = SubmitField("Let's go!")


class LoginForm(FlaskForm):
    login = StringField("Login (e-mail)", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Let's go!")


class CommentForm(FlaskForm):
    __form__ = 'comment'
    text = StringField("write a comment...", validators=[DataRequired()])


class QAAForm(FlaskForm):
    __form__ = 'qaa'
    title = StringField('What is the problem? Be short', validators=[DataRequired()])
    text = TextAreaField(validators=[DataRequired()])
    tags = StringField()
    submit = SubmitField("Post")


class AnswerForm(FlaskForm):
    __form__ = 'answ'
    text = StringField("write an answer...", validators=[DataRequired()])
