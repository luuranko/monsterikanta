from application import db
from application.models import Base
from flask_login import current_user

from sqlalchemy import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    monsters = db.relationship("Monster", backref="account", lazy=True)
    enviros = db.relationship("Enviro", backref="account", lazy=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def users_with_most_monsters():
        stmt = text("SELECT Account.name, COUNT(Monster.id) AS monster FROM Account" " LEFT JOIN Monster ON Account.id = Monster.account_id" " GROUP BY Account.name" " ORDER BY monster DESC")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "id":row[1]})
        return response

    @staticmethod
    def users_with_most_enviros():
        stmt = text("SELECT Account.name, COUNT(Enviro.id) AS enviro FROM Account" " LEFT JOIN Enviro ON Account.id = Enviro.account_id" " GROUP BY Account.name" " ORDER BY enviro DESC")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"name":row[0], "id":row[1]})
        return response
