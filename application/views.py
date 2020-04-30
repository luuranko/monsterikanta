from flask import render_template
from application import app
from flask_login import current_user
from application.auth.models import User

@app.route("/")
def index():

    if current_user.is_authenticated:
        monster = User.latest_monster(current_user.id)
        print(monster)
        enviro = User.latest_enviro(current_user.id)
        print(enviro)
        users = User.m_rankings()
        e_users = User.e_rankings()
        for i in range(len(users)):
            name = users[i].get("name")
            index = 0
            for e in e_users:
                if e.get("name") == name:
                    index = e_users.index(e)
            users[i].update(e_users[index])

        return render_template("index.html",
        monster = monster, enviro = enviro,
        users = users)
    else:
        return render_template("index.html")
