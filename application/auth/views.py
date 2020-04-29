from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required
from application.auth.models import User
from application.monsters.models import Monster, Trait, Action, Reaction, Legendary
from application.enviros.models import Enviro, EnviroMonster
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

    if len(form.name.data.strip()) < 3 or len(form.username.data.strip()) < 3 or len(form.password.data.strip()) < 3:
        return render_template("auth/newaccountform.html", form = form, error = "Your input must include at least 3 characters.")

    u_exists = User.query.filter_by(username=form.username.data.strip()).first()
    if u_exists:
        return render_template("auth/newaccountform.html", form = form, error = "This username is already taken.")

    n_exists = User.query.filter_by(name=form.name.data.strip()).first()
    if n_exists:
        return render_template("auth/newaccountform.html", form = form, error="This name is already taken.")

    u = User(form.name.data.strip(), form.username.data.strip(), form.password.data.strip())
    db.session().add(u)
    db.session().commit()
    login_user(u)

    return redirect(url_for("index"))

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

@app.route("/auth/admin/users")
@login_required(role="ADMIN")
def admin_users():

    if not current_user.is_admin():
        return redirect(url_for("index"))

    users = User.query.filter(User.admin==False)

    return render_template("auth/admin_users.html", users = users)

@app.route("/auth/admin/delete/<account_id>", methods=["POST"])
@login_required(role="ADMIN")
def admin_delete_user(account_id):

    u = User.query.get(account_id)
    if not u:
        redirect(url_for('admin_users'))

    monsters = u.own_monsters(u.id)

    for mon in monsters:
        m = Monster.query.get(mon['id'])
        traits = m.this_traits(m.id)
        for t in traits:
            db.session().delete(Trait.query.get(t['id']))
            db.session().commit()
        actions =  m.this_actions(m.id)
        for a in actions:
            db.session().delete(Action.query.get(a['id']))
            db.session().commit()
        reactions = m.this_reactions(m.id)
        for r in reactions:
            db.session().delete(Reaction.query.get(r['id']))
            db.session().commit()
        legendaries = m.this_legendaries(m.id)
        for l in legendaries:
            db.session().delete(Legendary.query.get(l['id']))
            db.session().commit()
        em = EnviroMonster.query.all()
        for i in em:
            if i.monster_id == m.id:
                db.session().delete(i)
                db.session().commit()
        db.session().delete(m)
        db.session().commit()

    enviros = u.own_enviros(u.id)

    for env in enviros:
        e = Enviro.query.get(env['id'])
        db.session().delete(e)
        db.session().commit()

    db.session().delete(u)
    db.session().commit()

    return redirect(url_for('admin_users'))
