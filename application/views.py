from flask import render_template
from application import app
from flask_login import current_user
from application.auth.models import User

@app.route("/")
def index():

    if current_user.is_authenticated:
        monster = User.latest_monster(current_user.id)
        enviro = User.latest_enviro(current_user.id)
        users = User.m_rankings()
        print(users)
        e_users = User.e_rankings()
        print(e_users)
        for i in range(len(users)):
            print(users[i])
            name = users[i].get("name")
            for e in e_users:
                if e.get("name") == name:
                    index = e_users.index(e)
                    users[i].update(e_users[index])
            print(users[i])

        return render_template("index.html",
        monster = monster, enviro = enviro,
        users = users)
    else:
        return render_template("index.html")
