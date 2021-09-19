from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class NewPostForm(FlaskForm):
	text = StringField("Enter the text", validators=[DataRequired()])
	submit = SubmitField("Send!")


class RegistrationForm(FlaskForm):
	name = StringField("Your name", validators=[DataRequired()])
	email = StringField("E-mail", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm password", validators=[DataRequired()])
	description = TextAreaField("Short description (you can fill it later)")
	submit = SubmitField("Sing up!")


class LoginForm(FlaskForm):
	login = StringField("Login (e-mail)", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember = BooleanField("Remember me", default=False)
	submit = SubmitField("Sing in")
