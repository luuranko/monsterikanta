from application import db
from application.models import Base
from application.monsters.models import Monster

from sqlalchemy.sql import text

class Enviro(Base):

    __tablename__ = "enviro"

    name = db.Column(db.String(144), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    etype = db.Column(db.String(200), nullable=False)
    descrip = db.Column(db.String(5000), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    account_name = db.Column(db.String(144), nullable=False)

    monsters = db.relationship("EnviroMonster", back_populates="enviro", cascade="all, delete-orphan")

    def __init__(self, name, etype, descrip):
        self.name = name
        self.etype = etype
        self.descrip = descrip

    @staticmethod
    def local_monsters(enviro_id):
        stmt = text("SELECT Monster.id, Monster.name, Monster.public FROM Enviro"
 " JOIN EnviroMonster ON EnviroMonster.enviro_id = Enviro.id"
 " JOIN Monster ON Monster.id = EnviroMonster.monster_id"
 " WHERE EnviroMonster.enviro_id = :enviro"
 " ORDER BY Monster.name").params(enviro=enviro_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "public":row[2]})
        return response

    @staticmethod
    def addable_monsters(enviro_id):
        stmt = text("SELECT Monster.id, Monster.name FROM Monster"
 " WHERE id NOT IN (SELECT Monster.id FROM Enviro"
 " JOIN EnviroMonster ON EnviroMonster.enviro_id = Enviro.id"
 " JOIN Monster ON Monster.id = EnviroMonster.monster_id"
 " WHERE EnviroMonster.enviro_id = :enviro)"
 " ORDER BY Monster.name").params(enviro=enviro_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1]})
        return response

    @staticmethod
    def search_by_type(account_id, etype):
        stmt = text("SELECT Enviro.id, Enviro.name, Enviro.etype,"
 " Enviro.public, Enviro.account_id, Enviro.account_name FROM Enviro"
 " WHERE Enviro.etype = :etype AND"
 " (Enviro.account_id = :account OR Enviro.public)").params(etype=etype, account=account_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "etype":row[2], "public":row[3], "account_id":row[4], "account_name":row[5]})
        return response

    @staticmethod
    def search_by_name(account_id, name):
        stmt = text("SELECT Enviro.id, Enviro.name, Enviro.etype,"
 " Enviro.public, Enviro.account_id, Enviro.account_name FROM Enviro"
 " WHERE Enviro.name LIKE :name AND"
 " (Enviro.account_id = :account OR Enviro.public)").params(account=account_id, name='%'+name+'%')
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "etype":row[2], "public":row[3], "account_id":row[4], "account_name":row[5]})
        return response

class EnviroMonster(db.Model):

    __tablename__ = "enviromonster"

    enviro_id = db.Column(db.Integer, db.ForeignKey("enviro.id"), primary_key=True, nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), primary_key=True, nullable=False)

    enviro = db.relationship("Enviro", back_populates="monsters")
    monster = db.relationship("Monster", back_populates="enviros")

    def __init__(self, enviro_id, monster_id):
        self.enviro_id = enviro_id
        self.monster_id = monster_id
