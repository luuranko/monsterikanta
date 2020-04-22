from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired()])
    password = PasswordField("Password", [validators.InputRequired()])

    class Meta:
        csrf = False

class SigninForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=3, max=20)])
    username = StringField("Username", [validators.Length(min=3, max=10)])
    password = PasswordField("Password", [validators.Length(min=3, max=12), validators.EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Repeat password")

    class Meta:
        csrf = False
