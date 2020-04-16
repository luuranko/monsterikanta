from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_, and_

from application import app, db
from application.monsters.models import Monster
from application.enviros.models import EnviroMonster
from application.monsters.models import Trait
from application.monsters.models import Action
from application.monsters.forms import MonsterForm

# Listaa kaikki julkiset tai omat monsterit
@app.route("/monsters", methods=["GET"])
@login_required
def monsters_index():

    monsters = Monster.query.filter(or_(Monster.account_id==current_user.id,
    Monster.public==True))
    users = current_user.users_with_most_monsters()

    if not monsters.first():
        return render_template("monsters/list.html", users = users)

    return render_template("monsters/list.html",
    users = users, monsters = monsters)

# Vie uuden monsterin luomissivulle
@app.route("/monsters/new/")
@login_required
def monsters_form():

    return render_template("monsters/new.html", form = MonsterForm())

# Luo oman monsterin
@app.route("/monsters/", methods=["POST"])
@login_required
def monsters_create():

    form = MonsterForm(request.form)

    if not form.validate():
        return render_template("monsters/new.html", form = form)

    real_name = form.name.data
    same = Monster.query.filter(and_(Monster.account_id==current_user.id, Monster.name==real_name))
    if same.first() is not None:
        number = same.count() + 1
        real_name = real_name + "#" + str(number)

    m = Monster(real_name, form.size.data, form.mtype.data,
   form.ac.data, form.hp.data, form.spd.data, form.stre.data,
   form.dex.data, form.con.data, form.inte.data, form.wis.data, form.cha.data,
   form.saves.data, form.skills.data, form.weakto.data, form.resist.data,
   form.immun.data, form.coimmun.data, form.sens.data, form.cr.data, form.descrip.data)

    m.public = form.public.data
    m.account_id = current_user.id
    m.account_name = current_user.name

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("monsters_index"))

# Muuttaa monsterin julkisuusasetuksen
@app.route("/monsters/toggle/<monster_id>/", methods=["POST"])
@login_required
def monsters_toggle_public(monster_id):


    m = Monster.query.get(monster_id)

    if m.account_id == current_user.id:
        m.public = not m.public
        db.session().commit()

    return redirect(url_for("monsters_show", monster_id = monster_id))

# Poistaa monsterin tietokannasta
@app.route("/monsters/remove/<monster_id>/", methods=["POST"])
@login_required
def monsters_remove(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    if m.account_id != current_user.id:
        return redirect(url_for("monsters_show", monster_id = monster_id))

    em = EnviroMonster.query.all()
    for i in em:
        if i.monster_id == monster_id:
            db.session.delete(i)
            db.session.commit()

    traits = m.this_traits(m.id)
    for t in traits:
       db.session.delete(Trait.query.get(t['id']))
       db.session().commit()

    actions = m.this_actions(m.id)
    for a in actions:
        db.session.delete(Action.query.get(a['id']))
        db.session().commit()

    db.session().delete(m)
    db.session().commit()

    return redirect(url_for("monsters_index"))


# Vie tietyn monsterin sivulle
@app.route("/monsters/<monster_id>/", methods=["GET"])
@login_required
def monsters_show(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    traits = m.this_traits(m.id)
    actions = m.this_actions(m.id)

    for a in actions:
        if a.get("name") == "Multiattack":
            actions.insert(0, actions.pop(actions.index(a)))

    return render_template("monsters/monster.html",
    monster = m, traits = traits, actions = actions)

# Vie tietyn monsterin muokkaussivulle
@app.route("/monsters/edit/<monster_id>/<contents>", methods=["GET"])
@login_required
def monsters_edit(monster_id, **contents):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    if m.account_id != current_user.id:
        return redirect(url_for("monsters_index"))

    contents = contents.get("contents")
    list = contents.split("%&%")
    if len(list) < 2:
        contents = {
            "name" : m.name,
            "size" : m.size,
            "mtype" : m.mtype,
            "ac" : m.ac,
            "hp" : m.hp,
            "spd" : m.spd,
            "stre" : m.stre,
            "dex" : m.dex,
            "con" : m.con,
            "inte" : m.inte,
            "wis" : m.wis,
            "cha" : m.cha,
            "saves" : m.saves,
            "skills" : m.skills,
            "weakto" : m.weakto,
            "resist" : m.resist,
            "immun" : m.immun,
            "coimmun" : m.coimmun,
            "sens" : m.sens,
            "cr" : m.cr,
            "descrip" : m.descrip,
            "public" : m.public
        }
    else:
        contents = {}
        for i in list:
            parts = i.split("¤")
            contents[parts[0]] = parts[1]

    size_choices = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]
    type_choices = ["Aberration", "Beast", "Celestial", "Construct",
    "Dragon", "Elemental", "Fey", "Fiend", "Giant", "Humanoid",
    "Monstrosity", "Ooze", "Plant", "Undead"]
    cr_choices = ["0", "1/8", "1/4", "1/2", "1", "2", "3", "4",
    "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
    "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
    "26", "27", "28", "29", "30"]
    traits = m.this_traits(m.id)
    actions = m.this_actions(m.id)

    for a in actions:
        if a.get("name") == "Multiattack":
            actions.insert(0, actions.pop(actions.index(a)))

    return render_template("monsters/edit.html",
    monster = m, size_choices = size_choices,
    type_choices = type_choices, cr_choices = cr_choices,
    traits = traits, actions = actions,
    contents = contents, form = MonsterForm())

# Luo monsterille Traitin
@app.route("/monsters/edit/<monster_id>/trait", methods=["POST"])
@login_required
def monsters_create_trait(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    form = MonsterForm(request.form)

    t = Trait(request.form.get("t_title"), request.form.get("t_usage"), request.form.get("t_content"))
    t.monster_id = m.id

    db.session().add(t)
    db.session().commit()

    contents = "name¤" + form.name.data + "%&%"
    contents += "size¤" + form.size.data + "%&%"
    contents += "mtype¤" + form.mtype.data + "%&%"
    contents += "ac¤" + str(form.ac.data) + "%&%"
    contents += "hp¤" + str(form.hp.data) + "%&%"
    contents += "spd¤" + form.spd.data + "%&%"
    contents += "stre¤" + str(form.stre.data) + "%&%"
    contents += "dex¤" + str(form.dex.data) + "%&%"
    contents += "con¤" + str(form.con.data) + "%&%"
    contents += "inte¤" + str(form.inte.data) + "%&%"
    contents += "wis¤" + str(form.wis.data) + "%&%"
    contents += "cha¤" + str(form.cha.data) + "%&%"
    contents += "saves¤" + form.saves.data + "%&%"
    contents += "skills¤" + form.skills.data + "%&%"
    contents += "weakto¤" + form.weakto.data + "%&%"
    contents += "resist¤" + form.resist.data + "%&%"
    contents += "immun¤" + form.immun.data + "%&%"
    contents += "coimmun¤" + form.coimmun.data + "%&%"
    contents += "sens¤" + form.sens.data + "%&%"
    contents += "cr¤" + form.cr.data + "%&%"
    contents += "descrip¤" + form.descrip.data + "%&%"
    contents += "public¤" + str(form.public.data)

    return redirect(url_for("monsters_edit", monster_id=m.id,contents=contents))


# Poistaa monsterilta Traitin
@app.route("/monsters/edit/<monster_id>/trait/remove", methods=["POST"])
@login_required
def monsters_delete_trait(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    t = Trait.query.get(request.form.get("trait_id"))
    if not t:
        return redirect(url_for("monsters_index"))

    db.session().delete(t)
    db.session().commit()

    form = MonsterForm(request.form)

    contents = "name¤" + form.name.data + "%&%"
    contents += "size¤" + form.size.data + "%&%"
    contents += "mtype¤" + form.mtype.data + "%&%"
    contents += "ac¤" + str(form.ac.data) + "%&%"
    contents += "hp¤" + str(form.hp.data) + "%&%"
    contents += "spd¤" + form.spd.data + "%&%"
    contents += "stre¤" + str(form.stre.data) + "%&%"
    contents += "dex¤" + str(form.dex.data) + "%&%"
    contents += "con¤" + str(form.con.data) + "%&%"
    contents += "inte¤" + str(form.inte.data) + "%&%"
    contents += "wis¤" + str(form.wis.data) + "%&%"
    contents += "cha¤" + str(form.cha.data) + "%&%"
    contents += "saves¤" + form.saves.data + "%&%"
    contents += "skills¤" + form.skills.data + "%&%"
    contents += "weakto¤" + form.weakto.data + "%&%"
    contents += "resist¤" + form.resist.data + "%&%"
    contents += "immun¤" + form.immun.data + "%&%"
    contents += "coimmun¤" + form.coimmun.data + "%&%"
    contents += "sens¤" + form.sens.data + "%&%"
    contents += "cr¤" + form.cr.data + "%&%"
    contents += "descrip¤" + form.descrip.data + "%&%"
    contents += "public¤" + str(form.public.data)

    return redirect(url_for("monsters_edit", monster_id=m.id,contents=contents))


# Luo monsterille Actionin
@app.route("/monsters/edit/<monster_id>/action", methods=["POST"])
@login_required
def monsters_create_action(monster_id):


    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    form = MonsterForm(request.form)

    a = Action(request.form.get("a_title"), request.form.get("a_usage"), request.form.get("a_content"))
    a.monster_id = m.id

    db.session().add(a)
    db.session().commit()


    contents = "name¤" + form.name.data + "%&%"
    contents += "size¤" + form.size.data + "%&%"
    contents += "mtype¤" + form.mtype.data + "%&%"
    contents += "ac¤" + str(form.ac.data) + "%&%"
    contents += "hp¤" + str(form.hp.data) + "%&%"
    contents += "spd¤" + form.spd.data + "%&%"
    contents += "stre¤" + str(form.stre.data) + "%&%"
    contents += "dex¤" + str(form.dex.data) + "%&%"
    contents += "con¤" + str(form.con.data) + "%&%"
    contents += "inte¤" + str(form.inte.data) + "%&%"
    contents += "wis¤" + str(form.wis.data) + "%&%"
    contents += "cha¤" + str(form.cha.data) + "%&%"
    contents += "saves¤" + form.saves.data + "%&%"
    contents += "skills¤" + form.skills.data + "%&%"
    contents += "weakto¤" + form.weakto.data + "%&%"
    contents += "resist¤" + form.resist.data + "%&%"
    contents += "immun¤" + form.immun.data + "%&%"
    contents += "coimmun¤" + form.coimmun.data + "%&%"
    contents += "sens¤" + form.sens.data + "%&%"
    contents += "cr¤" + form.cr.data + "%&%"
    contents += "descrip¤" + form.descrip.data + "%&%"
    contents += "public¤" + str(form.public.data)

    return redirect(url_for("monsters_edit", monster_id=m.id,contents=contents))


# Poistaa monsterilta Actionin
@app.route("/monsters/edit/<monster_id>/action/remove", methods=["POST"])
@login_required
def monsters_delete_action(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    a = Action.query.get(request.form.get("action_id"))
    if not a:
        return redirect(url_for("monsters_index"))

    db.session().delete(a)
    db.session().commit()

    form = MonsterForm(request.form)

    contents = "name¤" + form.name.data + "%&%"
    contents += "size¤" + form.size.data + "%&%"
    contents += "mtype¤" + form.mtype.data + "%&%"
    contents += "ac¤" + str(form.ac.data) + "%&%"
    contents += "hp¤" + str(form.hp.data) + "%&%"
    contents += "spd¤" + form.spd.data + "%&%"
    contents += "stre¤" + str(form.stre.data) + "%&%"
    contents += "dex¤" + str(form.dex.data) + "%&%"
    contents += "con¤" + str(form.con.data) + "%&%"
    contents += "inte¤" + str(form.inte.data) + "%&%"
    contents += "wis¤" + str(form.wis.data) + "%&%"
    contents += "cha¤" + str(form.cha.data) + "%&%"
    contents += "saves¤" + form.saves.data + "%&%"
    contents += "skills¤" + form.skills.data + "%&%"
    contents += "weakto¤" + form.weakto.data + "%&%"
    contents += "resist¤" + form.resist.data + "%&%"
    contents += "immun¤" + form.immun.data + "%&%"
    contents += "coimmun¤" + form.coimmun.data + "%&%"
    contents += "sens¤" + form.sens.data + "%&%"
    contents += "cr¤" + form.cr.data + "%&%"
    contents += "descrip¤" + form.descrip.data + "%&%"
    contents += "public¤" + str(form.public.data)

    return redirect(url_for("monsters_edit", monster_id=m.id,contents=contents))



@app.route("/monsters/edit/<monster_id>/confirm", methods=["POST"])
@login_required
def monsters_commit_edit(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))
    form = MonsterForm(request.form)

    if not form.validate():
        contents = {
            "name" : form.name.data,
            "size" : form.size.data,
            "mtype" : form.mtype.data,
            "ac" : form.ac.data,
            "hp" : form.hp.data,
            "spd" : form.spd.data,
            "stre" : form.stre.data,
            "dex" : form.dex.data,
            "con" : form.con.data,
            "inte" : form.inte.data,
            "wis" : form.wis.data,
            "cha" : form.cha.data,
            "saves" : form.saves.data,
            "skills" : form.skills.data,
            "weakto" : form.weakto.data,
            "resist" : form.resist.data,
            "immun" : form.immun.data,
            "coimmun" : form.coimmun.data,
            "sens" : form.sens.data,
            "cr" : form.cr.data,
            "descrip" : form.descrip.data,
            "public" : form.public.data
        }

        return redirect(url_for("monsters_edit", monster_id=m.id,contents=contents))


    real_name = form.name.data
    same = Monster.query.filter(and_(Monster.account_id==current_user.id, Monster.name==real_name))
    if same.first() is not None and same.count() > 1:
        number = same.count() + 1
        real_name = real_name + "#" + str(number)

    m.name = real_name
    m.size = form.size.data
    m.mtype = form.mtype.data
    m.ac = form.ac.data
    m.hp = form.hp.data
    m.spd = form.spd.data
    m.stre = form.stre.data
    m.dex = form.dex.data
    m.con = form.con.data
    m.inte = form.inte.data
    m.wis = form.wis.data
    m.cha = form.cha.data
    m.saves = form.saves.data
    m.skills = form.skills.data
    m.weakto = form.weakto.data
    m.resist = form.resist.data
    m.immun = form.immun.data
    m.coimmun = form.coimmun.data
    m.sens = form.sens.data
    m.cr = form.cr.data
    m.descrip = form.descrip.data
    m.public = form.public.data

    db.session().commit()

    return redirect(url_for("monsters_index"))
