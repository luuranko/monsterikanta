from application import db
from application.models import Base
from application.monsters.models import Monster

from sqlalchemy.sql import text

class Enviro(Base):

    name = db.Column(db.String(144), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    etype = db.Column(db.String(200), nullable=False)
    descrip = db.Column(db.String(5000), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    account_name = db.Column(db.String(144), nullable=False)
    enviromonsters = db.relationship("EnviroMonster", backref="Enviro", lazy=True)

    def __init__(self, name, etype, descrip):
        self.name = name
        self.etype = etype
        self.descrip = descrip

    @staticmethod
    def local_monsters():
        stmt = text("SELECT Monster.id, Monster.name FROM Enviro"
 " JOIN enviro_monster ON enviro_monster.enviro_id = Enviro.id"
 " JOIN Monster ON Monster.id = enviro_monster.monster_id"
 " ORDER BY Monster.name")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1]})
        return response

    @staticmethod
    def addable_monsters():
        stmt = text("SELECT Monster.id, Monster.name FROM Monster"
 " WHERE id NOT IN (SELECT Monster.id FROM Enviro"
 " JOIN enviro_monster ON enviro_monster.enviro_id = Enviro.id"
 " JOIN Monster ON Monster.id = enviro_monster.monster_id)"
 " ORDER BY Monster.name")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1]})
        return response

class EnviroMonster(db.Model):

    enviro_id = db.Column(db.Integer, db.ForeignKey("enviro.id"), primary_key=True, nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), primary_key=True, nullable=False)

    def __init__(self, enviro, monster):
        self.enviro_id = enviro
        self.monster_id = monster
