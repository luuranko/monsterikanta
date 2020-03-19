from application import app, db
from flask import redirect, render_template, request, url_for
from application.monsters.models import Monster

@app.route("/monsters", methods=["GET"])
def monsters_index():
    return render_template("monsters/list.html", monsters = Monster.query.all())

@app.route("/monsters/new/")
def monsters_form():
    return render_template("monsters/new.html")

# Muuttaa monsterin julkisuusasetuksen yksityisestä julkiseksi
# hyödynnetään tulevaisuudessa siinä, että muut käyttäjät voivat
# nähdä ja tallentaa monsterin itselleen
@app.route("/monsters/<monster_id>/", methods=["POST"])
def monsters_set_public(monster_id):


    m = Monster.query.get(monster_id)
    m.public = True
    db.session().commit()

    return redirect(url_for("monsters_index"))

@app.route("/monsters/", methods=["POST"])
def monsters_create():
    m = Monster(request.form.get("name"), request.form.get("mtype"), request.form.get("size"), request.form.get("cr"), request.form.get("weakto"), request.form.get("resist"), request.form.get("descrip"), request.form.get("hp"), request.form.get("ac"), request.form.get("stre"), request.form.get("dex"), request.form.get("con"), request.form.get("inte"), request.form.get("wis"), request.form.get("cha"))

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("monsters_index"))
