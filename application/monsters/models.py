from application import db
from application.models import Base
from flask_login import current_user

from sqlalchemy.sql import text

class Monster(Base):

    __tablename__ = "monster"

    name = db.Column(db.String(144), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    mtype = db.Column(db.String(144), nullable=False)
    size = db.Column(db.String(144), nullable=False)
    cr = db.Column(db.String(144), nullable=False)
    weakto = db.Column(db.String(750))
    resist = db.Column(db.String(750))
    descrip = db.Column(db.String(5000))
    hp = db.Column(db.Integer, nullable=False)
    ac = db.Column(db.Integer, nullable=False)
    stre = db.Column(db.Integer, nullable=False)
    dex = db.Column(db.Integer, nullable=False)
    con = db.Column(db.Integer, nullable=False)
    inte = db.Column(db.Integer, nullable=False)
    wis = db.Column(db.Integer, nullable=False)
    cha = db.Column(db.Integer, nullable=False)
    sens = db.Column(db.String(500), nullable=False)
    spd = db.Column(db.String(100), nullable=False)
    saves = db.Column(db.String(144))
    skills = db.Column(db.String(750))
    immun = db.Column(db.String(750))
    coimmun = db.Column(db.String(750))
    l_points = db.Column(db.Integer)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    account_name = db.Column(db.String(144), nullable=False)

    enviros = db.relationship("EnviroMonster", back_populates="monster", cascade="all, delete-orphan")

    traits = db.relationship("Trait", backref="monster", lazy=True)
    actions = db.relationship("Action", backref="monster", lazy=True)
    reactions = db.relationship("Reaction", backref="monster", lazy=True)
    legendaries = db.relationship("Legendary", backref="monster", lazy=True)


    def __init__(self, name, size, mtype, ac, hp, spd, stre, dex, con, inte, wis, cha, saves, skills, weakto, resist, immun, coimmun, sens, cr, descrip):
        self.name = name
        self.size = size
        self.mtype = mtype
        self.ac = ac
        self.hp = hp
        self.spd = spd
        self.stre = stre
        self.dex = dex
        self.con = con
        self.inte = inte
        self.wis = wis
        self.cha = cha
        self.saves = saves
        self.skills = skills
        self.weakto = weakto
        self.resist = resist
        self.immun = immun
        self.coimmun = coimmun
        self.sens = sens
        self.cr = cr
        self.descrip = descrip

    @staticmethod
    def this_traits(monster_id):
        stmt = text("SELECT Trait.id, Trait.name, Trait.usage, Trait.content FROM Monster"
 " LEFT JOIN Trait ON Monster.id = Trait.monster_id"
 " WHERE Trait.monster_id = :monster"
 " ORDER BY LOWER(Trait.name)").params(monster=monster_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "usage":row[2], "content":row[3]})
        return response

    @staticmethod
    def this_actions(monster_id):
        stmt = text("SELECT Action.id, Action.name, Action.usage, Action.content, Action.atype FROM Monster"
 " LEFT JOIN Action ON Monster.id = Action.monster_id"
 " WHERE Action.monster_id = :monster"
 " ORDER BY Action.atype ASC, LOWER(Action.name)").params(monster=monster_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "usage":row[2], "content":row[3], "atype":row[4]})
        return response


    @staticmethod
    def this_reactions(monster_id):
        stmt = text("SELECT Reaction.id, Reaction.name, Reaction.content FROM Monster"
 " LEFT JOIN Reaction ON Monster.id = Reaction.monster_id"
 " WHERE Reaction.monster_id = :monster"
 " ORDER BY LOWER(Reaction.name)").params(monster=monster_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "content":row[2]})
        return response


    @staticmethod
    def this_legendaries(monster_id):
        stmt = text("SELECT Legendary.id, Legendary.name, Legendary.cost, Legendary.content FROM Monster"
 " LEFT JOIN Legendary ON Monster.id = Legendary.monster_id"
 " WHERE Legendary.monster_id = :monster"
 " ORDER BY LOWER(Legendary.name)").params(monster=monster_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1], "cost":row[2], "content":row[3]})
        return response

class Trait(Base):

    __tablename_ = "trait"

    name = db.Column(db.String(60), nullable=False)
    usage = db.Column(db.String(60), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), nullable=False)

    def __init__(self, name, usage, content):
        self.name = name
        self.usage = usage
        self.content = content


class Action(Base):

    __tablename_ = "action"

    name = db.Column(db.String(60), nullable=False)
    usage = db.Column(db.String(60), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    atype = db.Column(db.Integer, nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), nullable=False)

    def __init__(self, name, usage, content, atype):
        self.name = name
        self.usage = usage
        self.content = content
        self.atype = atype



class Reaction(Base):

    __tablename_ = "reaction"

    name = db.Column(db.String(60), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), nullable=False)

    def __init__(self, name, content):
        self.name = name
        self.content = content


class Legendary(Base):

    __tablename_ = "legendary"

    name = db.Column(db.String(60), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), nullable=False)

    def __init__(self, name, cost, content):
        self.name = name
        self.cost = cost
        self.content = content
