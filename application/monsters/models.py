from application import db
from application.models import Base
from flask_login import current_user

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
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    account_name = db.Column(db.String(144), nullable=False)

    enviros = db.relationship("EnviroMonster", back_populates="monster", cascade="all, delete-orphan")

    traits = db.relationship("Trait", backref="monster", lazy=True)
    actions = db.relationship("Action", backref="monster", lazy=True)

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

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    @staticmethod
    def get_monster_list():
        return Monster.query.filter(Monster.account_id==current_user.id)

class Trait(Base):

    name = db.Column(db.String(200), nullable=False)
    limit = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), nullable=False)

    def __init__(self, name, limit, content):
        self.name = name
        self.limit = limit
        self.content = content

class Action(Base):

    name = db.Column(db.String(200), nullable=False)
    limit = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), nullable=False)

    def __init__(self, name, limit, content):
        self.name = name
        self.limit = limit
        self.content = content
