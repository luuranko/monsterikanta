from application import db

class Monster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

# Monsterin nimi
    name = db.Column(db.String(144), nullable=False)
# Monsterin julkisuusasetus
    public = db.Column(db.Boolean, nullable=False)
# Monsterin tyyppi
    mtype = db.Column(db.String(144), nullable=False)
# Monsterin koko
    size = db.Column(db.String(144), nullable=False)
# Monsterin haastetaso
    cr = db.Column(db.String(144), nullable=False)
# Monsterin heikkoudet
    weakto = db.Column(db.String(144))
# Monsterin vahvuudet
    resist = db.Column(db.String(144))
# Monsterin sanallinen kuvaus
    descrip = db.Column(db.String(144))
# Monsterin Hit Pointit
    hp = db.Column(db.Integer, nullable=False)
# Monsterin Armor Class
    ac = db.Column(db.Integer, nullable=False)
# Monsterin Strength-stat
    stre = db.Column(db.Integer, nullable=False)
# Monsterin Dexterity-stat
    dex = db.Column(db.Integer, nullable=False)
# Monsterin Constitution-stat
    con = db.Column(db.Integer, nullable=False)
# Monsterin Intelligence-stat
    inte = db.Column(db.Integer, nullable=False)
# Monsterin Wisdom-stat
    wis = db.Column(db.Integer, nullable=False)
# Monsterin Charisma-stat
    cha = db.Column(db.Integer, nullable=False)
# Monsterin aistit
    sens = db.Column(db.String(200), nullable=False)
# Monsterin nopeudet
    spd = db.Column(db.String(200), nullable=False)
# Monsterin saving throwit
    saves = db.Column(db.String(144))
# Monsterin skillit
    skills = db.Column(db.String(144))
# Monsterin immuniteetit
    immun = db.Column(db.String(144))
# Monsterin statusimmuniteetit
    coimmun = db.Column(db.String(144))

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
