from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm
from application.auth.forms import SigninForm

@app.route("/auth/signin")
def auth_form():
    return render_template("auth/newaccountform.html", form = SigninForm())

@app.route("/auth/", methods=["POST"])
def auth_signin():
    form = SigninForm(request.form)

    if not form.validate():
        return render_template("auth/newaccountform.html", form = form)

    exists = User.query.filter_by(username=form.username.data).first()
    if exists:
        return render_template("auth/newaccountform.html", form = form, error = "Username not available")

    u = User(form.name.data, form.username.data, form.password.data)

    db.session().add(u)
    db.session().commit()

    return redirect(url_for("auth_login"))

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/loginform.html", form = form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form, error = "Incorrect  username or password")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))
