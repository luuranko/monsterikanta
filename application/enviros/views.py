from flask import redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import or_, and_

from application import app, db, login_required
from application.enviros.models import Enviro, EnviroMonster
from application.monsters.models import Monster
from application.enviros.forms import EnviroForm, SearchEnviroForm
from application.auth.models import User

@app.route("/enviros", methods=["GET", "POST"])
@login_required
def enviros_index():

    state = "-1"
    if request.method == "GET":
        form = SearchEnviroForm()
    else:
        form = SearchEnviroForm(request.form)
        state = form.whose.data

    if current_user.is_admin():
        if state == "-1":
            empty = ""
            enviros = Enviro.search_admin(state, current_user.id, empty, empty, empty)
        else:
            enviros = Enviro.search_admin(state, current_user.id, form.name.data, form.etype.data, form.owner.data)
    else:
        if state == "-1":
            empty = ""
            enviros = Enviro.search(state, current_user.id, empty, empty, empty)
        else:
            enviros = Enviro.search(state, current_user.id, form.name.data, form.etype.data, form.owner.data)

    def divideList(array, groupsize):
        if len(array) % groupsize != 0:
            pages = int(len(array) / groupsize + 1)
        else:
            pages = int(len(array) / groupsize)
        list = []
        for i in range(pages):
            list.append([])
        i = 0
        counter = 0
        for en in array:
            list[i].append(en)
            counter += 1
            if counter == groupsize:
                counter = 0
                i += 1
        return list

    if not enviros:
        lists = []
    else:
        lists = divideList(enviros, 10)
    pages = len(lists)

    return render_template("enviros/list.html",
    lists = lists, form = form, pages = pages)

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

    real_name = form.name.data.strip()
    if len(real_name) < 2:
        return render_template("enviros/new.html", form = form, error = "Name must be at least 2 characters long.")
    same = Enviro.query.filter(Enviro.account_id==current_user.id).filter(or_(Enviro.name==real_name, Enviro.name.like("{}#%".format(real_name))))
    if same.first() is not None:
        number = same.count() + 1
        real_name = real_name + "#" + str(number)
    e = Enviro(real_name, form.etype.data, form.descrip.data.strip())

    e.public = form.public.data
    e.account_id = current_user.id
    e.account_name = current_user.name

    db.session().add(e)
    db.session().commit()

    return redirect(url_for("enviros_show", enviro_id = e.id))

@app.route("/enviros/toggle/<enviro_id>/", methods=["POST"])
@login_required
def enviros_toggle_public(enviro_id):

    e = Enviro.query.get(enviro_id)

    if e.account.id == current_user.id or current_user.is_admin():
        e.public = not e.public
        db.session().commit()

    return redirect(url_for("enviros_show", enviro_id = enviro_id))

@app.route("/enviros/remove/<enviro_id>/", methods=["POST"])
@login_required
def enviros_remove(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))

    if e.account_id != current_user.id and not current_user.is_admin():
        return redirect(url_for("enviros_show", enviro_id = e.id))

    em = EnviroMonster.query.all()
    for i in em:
        if i.enviro_id == enviro_id:
            db.session.delete(i)
            db.session.commit()

    db.session().delete(e)
    db.session().commit()

    return redirect(url_for("enviros_index"))

@app.route("/enviros/<enviro_id>/", methods=["GET"])
@login_required
def enviros_show(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))

    local_monsters = Enviro.local_monsters(e.id)
    all_monsters = Enviro.addable_monsters(e.id, e.account_id)

    authorized = current_user.id == e.account_id or current_user.is_admin()

    return render_template("enviros/enviro.html", enviro = e,
    local_monsters = local_monsters, all_monsters = all_monsters,
    authorized = authorized)

@app.route("/enviros/<enviro_id>/add_monster/", methods=["GET", "POST"])
@login_required
def enviros_add_monster(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))

    m = Monster.query.get(request.values.get("addmon"))
    if m is None:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

    if (current_user.id != e.account_id or current_user.id != m.account_id) and not current_user.is_admin():
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

    if (current_user.id != e.account_id or current_user.id != m.account_id) and not current_user.is_admin():
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

    em = EnviroMonster.query.filter(and_(EnviroMonster.enviro_id==e.id, EnviroMonster.monster_id==m.id)).first()
    if em is None:
        return redirect(url_for("enviros_show", enviro_id = enviro_id))

    db.session().delete(em)
    db.session().commit()

    return redirect(url_for("enviros_show", enviro_id = enviro_id))

@app.route("/enviros/edit/<enviro_id>", methods=["GET", "POST"])
@login_required
def enviros_edit(enviro_id):

    e = Enviro.query.get(enviro_id)
    if e is None:
        return redirect(url_for("enviros_index"))

    if e.account_id != current_user.id and not current_user.is_admin():
        return redirect(url_for("enviros_index"))

    etype_choices = ["Arctic", "Coastal", "Desert", "Forest", "Grassland",
    "Hill", "Mountain", "Swamp", "Underground", "Underwater", "Urban"]

    if request.method == "GET":
        return render_template("enviros/edit.html",
        enviro = e, etype_choices = etype_choices, form = EnviroForm())

    form = EnviroForm(request.form)

    if not form.validate():
        return render_template("enviros/edit.html",
        enviro = e, etype_choices = etype_choices, form = EnviroForm())

    real_name = form.name.data.strip()
    if len(real_name) < 2:
        return render_template("enviros/edit.html", enviro = e, etype_choices = etype_choices, form = form, error = "Name must be at least 2 characters long.")
    same = Enviro.query.filter(Enviro.account_id==current_user.id).filter(or_(Enviro.name==real_name, Enviro.name.like("{}#%".format(real_name))))
    if same.first() is not None and same.count() > 1:
        number = same.count() + 1
        real_name = real_name + "#" + str(number)

    e.name = real_name
    e.etype = form.etype.data
    e.descrip = form.descrip.data.strip()
    e.public = form.public.data

    db.session().commit()

    return redirect(url_for("enviros_show", enviro_id = e.id))
