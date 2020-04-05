from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_

from application import app, db
from application.monsters.models import Monster
from application.monsters.forms import MonsterForm
from application.monsters.forms import TraitForm

# Listaa kaikki julkiset tai omat monsterit
@app.route("/monsters", methods=["GET"])
@login_required
def monsters_index():
    return render_template("monsters/list.html",
     monsters = Monster.query.filter(or_(Monster.account_id==current_user.id, Monster.public==True)))

# Vie uuden monsterin luomissivulle
@app.route("/monsters/new/")
@login_required
def monsters_form():
    return render_template("monsters/new.html", form = MonsterForm())

# Näyttää piirteenluontinäkymän
#@app.route("/monsters/new/trait/", methods=["GET"])
#@login_required
#def monsters_trait(monster_id):
#    monster = Monster.query.get(monster_id)
#    return render_template("monsters/trait.html", monster=monster, form = TraitForm())

# Luo piirteen
#@app.route("/monsters/new/trait/create/", methods=["POST"])
#@login_required
#def monsters_trait_creation(monster_id):
#    monster = Monster.query.get(monster_id)
#    form = TraitForm(request.form)
#    t = Trait(form.name.data, form.limit.data, form.content.data)
#    t.monster_id = monster.id
#    return redirect(url_for("monsters_edit", monster_id=monster.id))

# Luo oman monsterin
@app.route("/monsters/", methods=["POST"])
@login_required
def monsters_create():
    form = MonsterForm(request.form)

    if not form.validate():
        return render_template("monsters/new.html", form = form)

    m = Monster(form.name.data, form.size.data, form.mtype.data,
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
# Jos asettaa oman monsterin julkiseksi, muutkin käyttäjät näkevät sen listassa
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
    if m is None:
        return redirect(url_for("monsters_index"))

    if m.account_id == current_user.id:
        db.session().delete(m)
        db.session().commit()
        return redirect(url_for("monsters_index"))
    else:
        return redirect(url_for("monsters_show", monster_id = monster_id))

# Vie tietyn monsterin sivulle
@app.route("/monsters/<monster_id>/", methods=["GET"])
@login_required
def monsters_show(monster_id):

    m = Monster.query.get(monster_id)
    if m is None:
        return redirect(url_for("monsters_index"))
    else:
        return render_template("monsters/monster.html", monster = m)

# Vie tietyn monsterin muokkaussivulle
@app.route("/monsters/edit/<monster_id>/", methods=["GET"])
@login_required
def monsters_edit(monster_id):

    m = Monster.query.get(monster_id)
    if m is None:
        return redirect(url_for("monsters_index"))

    if m.account_id != current_user.id:
        return redirect(url_for("monsters_index"))
    else:
        return render_template("monsters/edit.html",
        monster = m, form = MonsterForm())

@app.route("/monsters/edit/<monster_id>/confirm", methods=["POST"])
@login_required
def monsters_commit_edit(monster_id):

    m = Monster.query.get(monster_id)
    form = MonsterForm(request.form)

    if not form.validate():
       return render_template("monsters/edit.html", monster = m, form = form)

    m.name = form.name.data
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

# Haut
@app.route("/monsters/most/", methods=["GET"])
@login_required
def monsters_most():
    return render_template("monsters/mostquery.html",
    users = current_user.users_with_most_monsters(),
    monsters =  Monster.query.filter(or_(Monster.account_id==current_user.id, Monster.public==True)))
