from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SelectField, IntegerField, BooleanField

class MonsterForm(FlaskForm):
    name = StringField("Monster name:", [validators.Length(min=2)])
    descrip = TextAreaField("Description:", [validators.Length(min=2)])
    mtype = SelectField("Type:", choices=[("Aberration", "Aberration"), ("Beast", "Beast"), ("Celestial", "Celestial"), ("Construct", "Construct"), ("Dragon", "Dragon"), ("Elemental", "Elemental"), ("Fey", "Fey"), ("Fiend", "Fiend"), ("Giant", "Giant"), ("Humanoid", "Humanoid"), ("Monstrosity", "Monstrosity"), ("Ooze", "Ooze"), ("Plant", "Plant"), ("Undead", "Undead")])
    size = SelectField("Size:", choices=[("Tiny", "Tiny"), ("Small", "Small"), ("Medium", "Medium"), ("Large", "Large"), ("Huge", "Huge"), ("Gargantuan", "Gargantuan")])
    cr = SelectField("Challenge Rating:", choices=[("0", "0"), ("1/8", "1/8"), ("1/4", "1/4"), ("1/2", "1/2"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"), ("11", "11"), ("12", "12"), ("13", "13"), ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"), ("18", "18"), ("19", "19"), ("20", "20"), ("21", "21"), ("22", "22"), ("23", "23"), ("24", "24"), ("25", "25")])
    weakto = StringField("Vulnerabilities:")
    resist = StringField("Resistances:")
    hp = IntegerField("Hit Points:", [validators.NumberRange(min=1, max=1000)])
    ac = IntegerField("Armor Class:", [validators.NumberRange(min=1, max=30)])
    stre = IntegerField("Strength:", [validators.NumberRange(min=1, max=30)])
    dex = IntegerField("Dexterity:", [validators.NumberRange(min=1, max=30)])
    con = IntegerField("Constitution:", [validators.NumberRange(min=1, max=30)])
    inte = IntegerField("Intelligence:", [validators.NumberRange(min=1, max=30)])
    wis = IntegerField("Wisdom:", [validators.NumberRange(min=1, max=30)])
    cha = IntegerField("Charisma:", [validators.NumberRange(min=1, max=30)])
    public = BooleanField("Make public?")

    class Meta:
        csrf = False