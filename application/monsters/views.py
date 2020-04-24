from flask import redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import or_, and_

from application import app, db, login_required
from application.monsters.models import Monster
from application.enviros.models import EnviroMonster
from application.monsters.models import Trait
from application.monsters.models import Action
from application.monsters.models import Reaction
from application.monsters.models import Legendary
from application.monsters.forms import MonsterForm

# Listaa kaikki julkiset tai omat monsterit
@app.route("/monsters", methods=["GET"])
@login_required
def monsters_index():

    if current_user.is_admin():
        monsters = Monster.query.all()
    else:
        monsters = Monster.query.filter(or_(Monster.account_id==current_user.id,
        Monster.public==True))
    users = current_user.users_with_most_monsters()

    if current_user.is_admin() and not monsters:
       return render_template("monsters/list.html", users = users)
    if not current_user.is_admin() and not monsters.first():
        return render_template("monsters/list.html", users = users)

    size_choices = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]

    return render_template("monsters/list.html",
    users = users, monsters = monsters,
    size_choices = size_choices)

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
    same = Monster.query.filter(Monster.account_id==current_user.id).filter(or_(Monster.name == real_name, Monster.name.like("{}#%".format(real_name))))
    if same.first() is not None:
        number = same.count() + 1
        real_name = real_name + "#" + str(number)

    m = Monster(real_name, form.size.data, form.mtype.data,
   form.ac.data, form.hp.data, form.spd.data, form.stre.data,
   form.dex.data, form.con.data, form.inte.data, form.wis.data, form.cha.data,
   form.saves.data, form.skills.data, form.weakto.data, form.resist.data,
   form.immun.data, form.coimmun.data, form.sens.data, form.cr.data, form.descrip.data)

    if request.form.get("legendary_check") == "on" and int(request.form.get("l_points")) > 0:
        m.l_points = request.form.get("l_points")
    else:
        m.l_points = 0

    m.public = form.public.data
    m.account_id = current_user.id
    m.account_name = current_user.name

    db.session().add(m)
    db.session().commit()

    # Noudetaan Traitit ja luodaan ne
    traits = request.form.get("return_traits")
    list = traits.split("£")
    for i in list:
        if i != "":
            parts = i.split("¤")
            t = Trait(parts[0], parts[1], parts[2])
            t.monster_id = m.id
            db.session().add(t)
            db.session().commit()

    # Noudetaan Actionit ja luodaan ne
    actions = request.form.get("return_actions")
    list = actions.split("£")
    for i in list:
        if i != "":
            parts = i.split("¤")
            a = Action(parts[0], parts[1], parts[2], parts[3])
            a.monster_id = m.id
            db.session().add(a)
            db.session().commit()

    # Noudetaan Reactionit ja luodaan ne
    reactions = request.form.get("return_reactions")
    list = reactions.split("£")
    for i in list:
        if i != "":
            parts = i.split("¤")
            r = Reaction(parts[0], parts[1])
            r.monster_id = m.id
            db.session().add(r)
            db.session().commit()

    # Noudetaan Legendary Actionit ja luodaan ne
    legendaries = request.form.get("return_legendaries")
    list = legendaries.split("£")
    for i in list:
        if i != "":
            parts = i.split("¤")
            l = Legendary(parts[0], int(parts[1]), parts[2])
            l.monster_id = m.id
            db.session().add(l)
            db.session().commit()


    return redirect(url_for("monsters_show", monster_id = m.id))

# Muuttaa monsterin julkisuusasetuksen
@app.route("/monsters/<monster_id>/toggle", methods=["POST"])
@login_required
def monsters_toggle_public(monster_id):


    m = Monster.query.get(monster_id)

    if m.account_id == current_user.id or current_user.is_admin():
        m.public = not m.public
        db.session().commit()

    return redirect(url_for("monsters_show", monster_id = monster_id))

# Poistaa monsterin tietokannasta
@app.route("/monsters/<monster_id>/remove", methods=["POST"])
@login_required
def monsters_remove(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    if m.account_id != current_user.id and not current_user.is_admin():
        return redirect(url_for("monsters_show", monster_id = monster_id))

    em = EnviroMonster.query.all()
    for i in em:
        if i.monster_id == monster_id:
            db.session().delete(i)
            db.session().commit()

    traits = m.this_traits(m.id)
    for t in traits:
       db.session().delete(Trait.query.get(t['id']))
       db.session().commit()

    actions = m.this_actions(m.id)
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

    db.session().delete(m)
    db.session().commit()

    return redirect(url_for("monsters_index"))


# Vie tietyn monsterin sivulle
@app.route("/monsters/<monster_id>", methods=["GET"])
@login_required
def monsters_show(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    traits = m.this_traits(m.id)
    actions = m.this_actions(m.id)
    reactions = m.this_reactions(m.id)
    legendaries = m.this_legendaries(m.id)

    for a in actions:
        if a.get("name") == "Multiattack":
            actions.insert(0, actions.pop(actions.index(a)))

    authorized = current_user.id == m.account_id or current_user.is_admin()

    return render_template("monsters/monster.html",
    monster = m, traits = traits, actions = actions,
    reactions = reactions, legendaries = legendaries,
    authorized = authorized)

# Monsterin muokkaussivu
@app.route("/monsters/<monster_id>/edit", methods=["GET", "POST"])
@login_required
def monsters_edit(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
        return redirect(url_for("monsters_index"))

    if m.account_id != current_user.id and not current_user.is_admin():
        return redirect(url_for("monsters_index"))

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
    reactions = m.this_reactions(m.id)
    legendaries = m.this_legendaries(m.id)

    if request.method == "GET":
        return render_template("monsters/edit.html",
        monster = m, size_choices = size_choices,
        type_choices = type_choices, cr_choices = cr_choices,
        pre_traits = traits, pre_actions = actions,
        pre_reactions = reactions, pre_legendaries = legendaries,
        form = MonsterForm())

    form = MonsterForm(request.form)

    if not form.validate():
        return render_template("monsters/edit.html",
        monster = m, size_choices = size_choices,
        type_choices = type_choices, cr_choices = cr_choices,
        pre_traits = traits, pre_actions = actions,
        pre_reactions = reactions, pre_legendaries = legendaries,
        form = form)

    real_name = form.name.data
    same = Monster.query.filter(Monster.account_id==current_user.id).filter(or_(Monster.name == real_name, Monster.name.like("{}#%".format(real_name))))
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
    if request.form.get("legendary_check") == "on" and int(request.form.get("l_points")) > 0:
        m.l_points = request.form.get("l_points")
    else:
        m.l_points = 0
    m.descrip = form.descrip.data
    m.public = form.public.data

    db.session().commit()

    # Noudetaan Traitit ja luodaan ne
    traits = m.this_traits(m.id)
    for t in traits:
       db.session().delete(Trait.query.get(t['id']))
       db.session().commit()
    traits = request.form.get("return_traits")
    list = traits.split("£")
    for i in list:
        if i != "":
            parts = i.split("¤")
            if parts[0] != "" and parts[2] != '':
                t = Trait(parts[0], parts[1], parts[2])
                t.monster_id = m.id
                db.session().add(t)
                db.session().commit()

    # Noudetaan Actionit ja luodaan ne
    actions = m.this_actions(m.id)
    for a in actions:
        db.session().delete(Action.query.get(a['id']))
        db.session().commit()
    actions = request.form.get("return_actions")
    list = actions.split("£")
    for i in list:
        if i != "":
            parts = i.split("¤")
            a = Action(parts[0], parts[1], parts[2], parts[3])
            a.monster_id = m.id
            db.session().add(a)
            db.session().commit()

    # Noudetaan Reactionit ja luodaan ne
    reactions = m.this_reactions(m.id)
    for r in reactions:
        db.session().delete(Reaction.query.get(r['id']))
        db.session().commit()
    reactions = request.form.get("return_reactions")
    list = reactions.split("£")
    for i in list:
        if i != "":
            parts = i.split("¤")
            r = Reaction(parts[0], parts[1])
            r.monster_id = m.id
            db.session().add(r)
            db.session().commit()

    # Noudetaan Legendary Actionit ja luodaan ne
    legendaries = m.this_legendaries(m.id)
    for l in legendaries:
        db.session().delete(Legendary.query.get(l['id']))
        db.session().commit()
    legendaries = request.form.get("return_legendaries")
    list = legendaries.split("£")
    for i in list:
        if i != "":
            parts = i.split("¤")
            l = Legendary(parts[0], int(parts[1]), parts[2])
            l.monster_id = m.id
            db.session().add(l)
            db.session().commit()


    return redirect(url_for("monsters_show", monster_id = m.id))
