from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import or_

from application import app, db
from application.monsters.models import Monster
from application.monsters.forms import MonsterForm

# Listaa kaikki julkiset tai omat monsterit
@app.route("/monsters", methods=["GET"])
@login_required
def monsters_index():
    return render_template("monsters/list.html", monsters = Monster.query.filter(or_(Monster.account_id==current_user.id, Monster.public==True)))

# Vie uuden monsterin luomissivulle
@app.route("/monsters/new/")
@login_required
def monsters_form():
    return render_template("monsters/new.html", form = MonsterForm())

# Muuttaa monsterin julkisuusasetuksen
# Jos asettaa oman monsterin julkiseksi, muutkin käyttäjät näkevät sen listassa
@app.route("/monsters/<monster_id>/", methods=["POST"])
@login_required
def monsters_toggle_public(monster_id):


    m = Monster.query.get(monster_id)

    if m.account_id != current_user.id:
        return redirect(url_for("monsters_index"))

    if m.public == True:
        m.public = False
    else:
        m.public = True
    db.session().commit()

    return redirect(url_for("monsters_index"))

# Luo oman monsterin
@app.route("/monsters/", methods=["POST"])
@login_required
def monsters_create():
    form = MonsterForm(request.form)

    if not form.validate():
        return render_template("monsters/new.html", form = form)

    m = Monster(form.name.data, form.size.data, form.mtype.data, form.ac.data, form.hp.data, form.spd.data, form.stre.data, form.dex.data, form.con.data, form.inte.data, form.wis.data, form.cha.data, form.saves.data, form.skills.data, form.weakto.data, form.resist.data, form.immun.data, form.coimmun.data, form.sens.data, form.cr.data, form.descrip.data)

    m.public = form.public.data
    m.account_id = current_user.id

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("monsters_index"))


# @app.route("/monsters/edit/<monster_id>/", methods=["GET"])
# @login_required
# def monsters_edit(monster_id):

#    m = Monster.query.get(monster_id)


#    if m.account_id != current_user.id:
#        return redirect(url_for("monsters_index"))

#    return render_template("monsters/edit.html", form = EditMonsterForm())

# @app.route("/monsters/edit/", methods=["POST"])
# @login_required
# def monsters_edit():

#    form = EditMonsterForm(request.form)
