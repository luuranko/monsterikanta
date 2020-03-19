from application import db

class Monster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

# Monsterin nimi
    name = db.Column(db.String(144), nullable=False)
# Monsterin julkisuusasetus, aluksi false
    public = db.Column(db.Boolean, nullable=False)
# Monsterin tyyppi, myöhemmin muutetaan enum-muotoon Stringin sijaan
    mtype = db.Column(db.String(144), nullable=False)
# Monsterin koko, myöhemmin muutetaan enum-muotoon Stringin sijaan
    size = db.Column(db.String(144), nullable=False)
# Monsterin haastetaso, myöhemmin muutetaan enum-muotoon Integerin sijaan
    cr = db.Column(db.Integer, nullable=False)
# Monsterin heikkoudet listana, joka syötetään String-muodossa
    weakto = db.Column(db.String(144), nullable=False)
# Monsterin vahvuudet listana, joka syötetään String-muodossa 
    resist = db.Column(db.String(144), nullable=False)
# Monsterin sanallinen kuvaus
    descrip = db.Column(db.String(144), nullable=False)
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

    def __init__(self, name, mtype, size, cr, weakto, resist, descrip, hp, ac, stre, dex, con, inte, wis, cha):
        self.name = name
        self.public = False
        self.mtype = mtype
        self.size = size
        self.cr = cr
        self.weakto = weakto
        self.resist = resist
        self.descrip = descrip
        self.hp = hp
        self.ac = ac
        self.stre = stre
        self.dex = dex
        self.con = con
        self.inte = inte
        self.wis = wis
        self.cha = cha
