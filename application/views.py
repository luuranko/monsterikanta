from flask import render_template
from application import app
from flask_login import current_user
from application.auth.models import User

@app.route("/")
def index():

    if current_user.is_authenticated:
        monsters = User.own_monsters(current_user.id)
        enviros = User.own_enviros(current_user.id)
        if monsters and enviros:
            monster = monsters[0]
            enviro = enviros[0]
            return render_template("index.html", monster = monster, enviro = enviro)
        if monsters:
            monster = monsters[0]
            return render_template("index.html", monster = monster)
        if enviros:
            enviro = enviros[0]
            return render_template("index.html", enviro = enviro)
        return render_template("index.html")
    else:
        return render_template("index.html")
