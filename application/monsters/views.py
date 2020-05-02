from flask import redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import or_, and_

from application import app, db, login_required
from application.monsters.models import Monster, Trait, Action, Reaction, Legendary
from application.enviros.models import EnviroMonster
from application.monsters.forms import MonsterForm, SearchMonsterForm

# Monsterien listaus ja hakutoiminnallisuus
@app.route("/monsters", methods=["GET", "POST"])
@login_required
def monsters_index():

    state = "-1"
    if request.method == "GET":
        form = SearchMonsterForm()
    else:
        form = SearchMonsterForm(request.form)
        state = form.whose.data

    if current_user.is_admin():
        if state == "-1":
            empty = ""
            monsters = Monster.search_admin(state, current_user.id, empty, empty, empty, empty, "0", empty)
        else:
            monsters = Monster.search_admin(state, current_user.id, form.name.data, form.size.data, form.mtype.data, form.cr.data, form.legendary.data, form.owner.data)
    else:
        if state == "-1":
            empty = ""
            monsters = Monster.search(state, current_user.id, empty, empty, empty, empty, "0", empty)
        else:
            monsters = Monster.search(state, current_user.id, form.name.data, form.size.data, form.mtype.data, form.cr.data, form.legendary.data, form.owner.data)

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
        for mon in array:
            list[i].append(mon)
            counter += 1
            if counter == groupsize:
                counter = 0
                i += 1
        return list

    if not monsters:
        lists = []
    else:
        lists = divideList(monsters, 10)
    pages = len(lists)

    return render_template("monsters/list.html",
    lists = lists, form = form, pages = pages)

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

    real_name = form.name.data.strip()
    if len(real_name) < 1:
        return render_template("monsters/new.html", form = form, error = "Name must not be empty.")
    same = Monster.query.filter(Monster.account_id==current_user.id).filter(or_(Monster.name == real_name, Monster.name.like("{}#%".format(real_name))))
    if same.first() is not None:
        number = same.count() + 1
        real_name = real_name + "#" + str(number)

    m = Monster(real_name, form.size.data, form.mtype.data,
   form.ac.data, form.hp.data, form.spd.data.strip(), form.stre.data,
   form.dex.data, form.con.data, form.inte.data, form.wis.data, form.cha.data,
   form.saves.data.strip(), form.skills.data.strip(), form.weakto.data.strip(), form.resist.data.strip(),
   form.immun.data.strip(), form.coimmun.data.strip(), form.sens.data.strip(), form.cr.data, form.descrip.data.strip())

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

# Ability Score modifiers
def modifiers():

    table = {
      1: "-5",
      2: "-4",
      3: "-4",
      4: "-3",
      5: "-3",
      6: "-2",
      7: "-2",
      8: "-1",
      9: "-1",
      10: "+0",
      11: "+0",
      12: "+1",
      13: "+1",
      14: "+2",
      15: "+2",
      16: "+3",
      17: "+3",
      18: "+4",
      19: "+4",
      20: "+5",
      21: "+5",
      22: "+6",
      23: "+6",
      24: "+7",
      25: "+7",
      26: "+8",
      27: "+8",
      28: "+9",
      29: "+9",
      30: "+10"
    }

    return table

# Challenge Ratingin XP-määrät
def exp_amount():

    table = {
      "0": "10",
      "1/8": "25",
      "1/4": "50",
      "1/2": "100",
      "1": "200",
      "2": "450",
      "3": "700",
      "4": "1,100",
      "5": "1,800",
      "6": "2,300",
      "7": "2,900",
      "8": "3,900",
      "9": "5,000",
      "10": "5,900",
      "11": "7,200",
      "12": "8,400",
      "13": "10,000",
      "14": "11,500",
      "15": "13,000",
      "16": "15,000",
      "17": "18,000",
      "18": "20,000",
      "19": "22,000",
      "20": "25,000",
      "21": "33,000",
      "22": "41,000",
      "23": "50,000",
      "24": "62,000",
      "25": "75,000",
      "26": "90,000",
      "27": "105,000",
      "28": "120,000",
      "29": "135,000",
      "30": "155,000"
    }

    return table

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

    table = modifiers()
    mods = {
      "stre": table[m.stre],
      "dex": table[m.dex],
      "con": table[m.con],
      "inte": table[m.inte],
      "wis": table[m.wis],
      "cha": table[m.cha]
    }
    table = exp_amount()
    exp = table[str(m.cr)]

    return render_template("monsters/monster.html",
    monster = m, traits = traits, actions = actions,
    reactions = reactions, legendaries = legendaries,
    authorized = authorized, mods = mods, exp = exp)

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

    real_name = form.name.data.strip()
    same = Monster.query.filter(Monster.account_id==current_user.id).filter(or_(Monster.name == real_name, Monster.name.like("{}#%".format(real_name))))
    if same.first() is not None and same.count() > 1:
        number = same.count() + 1
        real_name = real_name + "#" + str(number)

    m.name = real_name
    m.size = form.size.data
    m.mtype = form.mtype.data
    m.ac = form.ac.data
    m.hp = form.hp.data
    m.spd = form.spd.data.strip()
    m.stre = form.stre.data
    m.dex = form.dex.data
    m.con = form.con.data
    m.inte = form.inte.data
    m.wis = form.wis.data
    m.cha = form.cha.data
    m.saves = form.saves.data.strip()
    m.skills = form.skills.data.strip()
    m.weakto = form.weakto.data.strip()
    m.resist = form.resist.data.strip()
    m.immun = form.immun.data.strip()
    m.coimmun = form.coimmun.data.strip()
    m.sens = form.sens.data.strip()
    m.cr = form.cr.data
    if request.form.get("legendary_check") == "on" and int(request.form.get("l_points")) > 0:
        m.l_points = request.form.get("l_points")
    else:
        m.l_points = 0
    m.descrip = form.descrip.data.strip()
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

# Monsterista kopion luominen ja sen muokkaaminen
@app.route("/monsters/<monster_id>/copy", methods=["GET", "POST"])
@login_required
def monsters_copy(monster_id):

    m = Monster.query.get(monster_id)
    if not m:
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
        form = MonsterForm(), copy = 1)

    form = MonsterForm(request.form)

    if not form.validate():
        return render_template("monsters/edit.html",
        monster = m, size_choices = size_choices,
        type_choices = type_choices, cr_choices = cr_choices,
        pre_traits = traits, pre_actions = actions,
        pre_reactions = reactions, pre_legendaries = legendaries,
        form = form, copy = 1)

    real_name = form.name.data.strip()
    same = Monster.query.filter(Monster.account_id==current_user.id).filter(or_(Monster.name == real_name, Monster.name.like("{}#%".format(real_name))))
    if same.first() is not None:
        number = same.count() + 1
        real_name = real_name + "#" + str(number)

    m = Monster(real_name, form.size.data, form.mtype.data,
    form.ac.data, form.hp.data, form.spd.data.strip(), form.stre.data,
    form.dex.data, form.con.data, form.inte.data, form.wis.data, form.cha.data,
    form.saves.data.strip(), form.skills.data.strip(), form.weakto.data.strip(), form.resist.data.strip(),
    form.immun.data.strip(), form.coimmun.data.strip(), form.sens.data.strip(), form.cr.data, form.descrip.data.strip())

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
            if parts[0] != "" and parts[2] != '':
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

