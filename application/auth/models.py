from application import db
from application.models import Base
from flask_login import current_user

from sqlalchemy import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    monsters = db.relationship("Monster", backref="account", lazy=True)
    enviros = db.relationship("Enviro", backref="account", lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.admin = False

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def is_admin(self):
        if self.admin:
            return True
        else:
            return False

    def roles(self):
        if self.admin:
            return ["ADMIN"]
        else:
            return ["USER"]

    @staticmethod
    def users_with_most_monsters():
        stmt = text("SELECT Account.name, COUNT(Monster.id) AS monster FROM Account"
 " LEFT JOIN Monster ON Account.id = Monster.account_id"
 " GROUP BY Account.name"
 " ORDER BY monster DESC")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "id":row[1]})
        return response

    @staticmethod
    def users_with_most_enviros():
        stmt = text("SELECT Account.name, COUNT(Enviro.id) AS enviro FROM Account"
 " LEFT JOIN Enviro ON Account.id = Enviro.account_id"
 " GROUP BY Account.name"
 " ORDER BY enviro DESC")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "id":row[1]})
        return response


    @staticmethod
    def own_monsters(account_id):
        stmt = text("SELECT Monster.id, Monster.name, Monster.date_modified FROM Account"
 " LEFT JOIN Monster ON Account.id = Monster.account_id"
 " WHERE Monster.account_id = :account"
 " ORDER BY Monster.date_modified DESC").params(account=account_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "date_modified":row[2]})
        return response

    @staticmethod
    def own_enviros(account_id):
        stmt = text("SELECT Enviro.id, Enviro.name, Enviro.date_modified FROM Account"
 " LEFT JOIN Enviro ON Account.id = Enviro.account_id"
 " WHERE Enviro.account_id = :account"
 " ORDER BY Enviro.date_modified DESC").params(account=account_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "date_modified":row[2]})
        return response

