from flask import render_template
from application import app
from flask_login import current_user
from application.auth.models import User

@app.route("/")
def index():

    if current_user.is_authenticated:
        monster = User.latest_monster(current_user.id)
        enviro = User.latest_enviro(current_user.id)

        users = User.query.all()
        dictlist = []
        for u in users:
            row = {"id":-1, "name":-1, "admin":-1, "monsters":0, "enviros":0}
            row.update(User.monstercount(u.id))
            row.update(User.envirocount(u.id))
            dictlist.append(row)
        dictlist = sorted(dictlist, key = lambda i: (-i['monsters'], -i['enviros'], i['name']))

        return render_template("index.html",
        monster = monster, enviro = enviro,
        users = dictlist)
    else:
        return render_template("index.html")
