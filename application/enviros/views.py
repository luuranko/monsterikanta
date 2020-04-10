from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_, and_

from application import app, db
from application.enviros.models import Enviro
from application.enviros.models import EnviroMonster
from application.monsters.models import Monster
from application.enviros.forms import EnviroForm
from application.auth.models import User

@app.route("/enviros", methods=["GET"])
@login_required
def enviros_index():

    enviros = Enviro.query.filter(or_(Enviro.account_id==current_user.id,
    Enviro.public==True))
    users = current_user.users_with_most_enviros()
    if enviros.first() is None:
        return render_template("enviros/list.html", users = users)
    return render_template("enviros/list.html",
    users = users, enviros = enviros)

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
        em = EnviroMonster.query.all()
        for i in em:
            if i.enviro_id == enviro_id:
                db.session.delete(i)
                db.session.commit()
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
    local_monsters = Enviro.local_monsters(e.id)
    return render_template("enviros/enviro.html", enviro = e,
    local_monsters = local_monsters)

@app.route("/enviros/<enviro_id>/add_monster", methods=["GET"])
@login_required
def enviros_manage_local_monsters(enviro_id):

    e = Enviro.query.get(enviro_id)
    all_monsters = e.addable_monsters(e.id)
    local_monsters = e.local_monsters(e.id)
    if not all_monsters and not local_monsters:
        return render_template("enviros/localmonsters.html", enviro = e)
    if not all_monsters:
        return render_template("enviros/localmonsters.html", enviro = e,
        local_monsters = local_monsters)
    if not local_monsters:
        return render_template("enviros/localmonsters.html", enviro = e, all_monsters = all_monsters)
    return render_template("enviros/localmonsters.html", enviro = e,
    all_monsters = all_monsters, local_monsters = local_monsters)

@app.route("/enviros/<enviro_id>/add_monster/", methods=["GET", "POST"])
@login_required
def enviros_add_monster(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))
    m = Monster.query.get(request.values.get("addmon"))
    if m is None:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))
    if current_user.id != e.account_id or current_user.id != m.account_id:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

    em = EnviroMonster(e.id, m.id)

    db.session().add(em)
    db.session().commit()

    return redirect(url_for("enviros_show", enviro_id = enviro_id))

@app.route("/enviros/<enviro_id>/remove_monster/", methods=["GET", "POST"])
@login_required
def enviros_remove_monster(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))
    m = Monster.query.get(request.values.get("removemon"))
    if m is None:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))
    if current_user.id != e.account_id or current_user.id != m.account_id:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

    em = EnviroMonster.query.filter(and_(EnviroMonster.enviro_id==e.id, EnviroMonster.monster_id==m.id)).first()
    if em is None:
        return redirect(url_for("enviros_manage_local_monsters", enviro_id = enviro_id))

    db.session().delete(em)
    db.session().commit()

    return redirect(url_for("enviros_show", enviro_id = enviro_id))

@app.route("/enviros/edit/<enviro_id>/", methods=["GET"])
@login_required
def enviros_edit(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))

    if e.account_id != current_user.id:
        return redirect(url_for("enviros_index"))

    etype_choices = ["Arctic", "Coastal", "Desert", "Forest", "Grassland",
    "Hill", "Mountain", "Swamp", "Underground", "Underwater", "Urban"]
    return render_template("enviros/edit.html",
    enviro = e, etype_choices = etype_choices, form = EnviroForm())

@app.route("/enviros/edit/<enviro_id>/confirm", methods=["POST"])
@login_required
def enviros_commit_edit(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e.account_id != current_user.id:
        redirect(url_for("enviros_show", enviro_id = e.id))

    form = EnviroForm(request.form)

    if not form.validate():
        etype_choices = ["Arctic", "Coastal", "Desert", "Forest", "Grassland",
        "Hill", "Mountain", "Swamp", "Underground", "Underwater", "Urban"]
        return render_template("enviros/edit.html",
        enviro = e, etype_choices = etype_choices, form = EnviroForm())

    e.name = form.name.data
    e.etype = form.etype.data
    e.descrip = form.descrip.data
    e.public = form.public.data

    db.session().commit()

    return redirect(url_for("enviros_show", enviro_id = e.id))

# Haut
@app.route("/enviros/most/", methods=["GET"])
@login_required
def enviros_most():

    enviros = Enviro.query.filter(or_(Enviro.account_id==current_user.id,
    Enviro.public==True))
    if enviros.first() is None:
        return render_template("enviros/mostquery.html",
    users = current_user.users_with_most_enviros())
    return render_template("enviros/mostquery.html",
    users = current_user.users_with_most_enviros(), enviros = enviros)
