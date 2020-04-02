from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_

from application import app, db
from application.enviros.models import Enviro
from application.enviros.models import EnviroMonster
from application.monsters.models import Monster
from application.enviros.forms import EnviroForm
from application.enviros.forms import EditEnviroForm
from application.enviros.forms import AddMonsterForm
from application.auth.models import User

@app.route("/enviros", methods=["GET"])
@login_required
def enviros_index():
    return render_template("enviros/list.html", enviros = Enviro.query.filter(or_(Enviro.account_id==current_user.id, Enviro.public==True)))

@app.route("/enviros/new/")
@login_required
def enviros_form():
    return render_template("enviros/new.html", form = EnviroForm())

@app.route("/enviros/", methods=["POST"])
@login_required
def enviros_create():
    form = EnviroForm(request.form)

    if not form.validate():
        return render_template("enviros/new.html", form = form)

    e = Enviro(form.name.data, form.etype.data, form.descrip.data)

    e.public = form.public.data
    e.account_id = current_user.id
    e.account_name = current_user.name

    db.session().add(e)
    db.session().commit()

    return redirect(url_for("enviros_index"))

@app.route("/enviros/toggle/<enviro_id>/", methods=["POST"])
@login_required
def enviros_toggle_public(enviro_id):

    e = Enviro.query.get(enviro_id)

    if e.account.id == current_user.id:
        if e.public == True:
            e.public = False
        else:
            e.public = True
        db.session().commit()
        return redirect(url_for("enviros_show", enviro_id = enviro_id))
    else:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

@app.route("/enviros/remove/<enviro_id>/", methods=["POST"])
@login_required
def enviros_remove(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))

    if e.account_id == current_user.id:
        db.session().delete(e)
        db.session().commit()
        return redirect(url_for("enviros_index"))
    else:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

@app.route("/enviros/<enviro_id>/", methods=["GET"])
@login_required
def enviros_show(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))
    else:
        all_monsters = Monster.query.filter(Monster.account_id==current_user.id)
#        choice_list=[(monster.id, monster.name) for monster in all_monsters]
        return render_template("enviros/enviro.html", all_monsters=all_monsters, enviro = e, local_monsters=Enviro.local_monsters(), form = AddMonsterForm())

@app.route("/enviros/edit/<enviro_id>/", methods=["GET"])
@login_required
def enviros_edit(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))

    if e.account_id != current_user.id:
        return redirect(url_for("enviros_index"))
    else:
        return render_template("enviros/edit.html", enviro = e, form = EditEnviroForm())

@app.route("/enviros/edit/<enviro_id>/confirm", methods=["POST"])
@login_required
def enviros_commit_edit(enviro_id):

    e = Enviro.query.get(enviro_id)
    form = EditEnviroForm(request.form)

    e.name = form.name.data
    e.etype = form.etype.data
    e.descrip = form.descrip.data
    e.public = form.public.data

    db.session().commit()

    return redirect(url_for("enviros_index"))

#@app.route("/enviros/<enviro_id>/monster/", methods=["GET"]
#@login_required
#def enviros_get_mons(enviro_id):

#    e = Enviro.query.get(enviro_id)
#    if e is None:
#        return redirect(url_for("enviros_index"))

#    return render_template

@app.route("/enviros/<enviro_id>/monster", methods=["GET", "POST"])
@login_required
def enviros_add_monster(enviro_id):
    form = AddMonsterForm(request.form)
    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))
    m = Monster.query.get(form.mon.data)
    if m is None:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

    if e.account_id != current_user.id:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

    if m.account_id != current_user.id:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

    em = EnviroMonster(enviro_id, monster_id)

    db.session().add(em)
    db.session().commit()
    return redirect(url_for("enviros_show", enviro_id = enviro_id))


# Haut
@app.route("/enviros/most/", methods=["GET"])
@login_required
def enviros_most():
    return render_template("enviros/mostquery.html", users = current_user.users_with_most_enviros(), enviros = Enviro.query.filter(or_(Enviro.account_id==current_user.id, Enviro.public==True)))