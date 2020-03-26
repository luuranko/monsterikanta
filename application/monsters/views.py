from application import app, db
from flask import redirect, render_template, request, url_for
from application.monsters.models import Monster
from application.monsters.forms import MonsterForm

@app.route("/monsters", methods=["GET"])
def monsters_index():
    return render_template("monsters/list.html", monsters = Monster.query.all())

@app.route("/monsters/new/")
def monsters_form():
    return render_template("monsters/new.html", form = MonsterForm())

# Muuttaa monsterin julkisuusasetuksen
# hyödynnetään tulevaisuudessa siinä, että muut käyttäjät voivat
# nähdä ja tallentaa monsterin itselleen
@app.route("/monsters/<monster_id>/", methods=["POST"])
def monsters_toggle_public(monster_id):


    m = Monster.query.get(monster_id)
    if m.public == True:
        m.public = False
    else:
        m.public = True
    db.session().commit()

    return redirect(url_for("monsters_index"))

@app.route("/monsters/", methods=["POST"])
def monsters_create():
    form = MonsterForm(request.form)

    if not form.validate():
        return render_template("monsters/new.html", form = form)

    m = Monster(form.name.data, form.size.data, form.mtype.data, form.ac.data, form.hp.data, form.spd.data, form.stre.data, form.dex.data, form.con.data, form.inte.data, form.wis.data, form.cha.data, form.saves.data, form.skills.data, form.weakto.data, form.resist.data, form.immun.data, form.coimmun.data, form.sens.data, form.cr.data, form.descrip.data)

    m.public = form.public.data

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("monsters_index"))
