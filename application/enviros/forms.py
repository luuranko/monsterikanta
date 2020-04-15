from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SelectField, BooleanField

class EnviroForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, max=25)])
    etype = SelectField("Type", choices=[("Arctic", "Arctic"), ("Coastal", "Coastal"),
    ("Desert", "Desert"), ("Forest", "Forest"), ("Grassland", "Grassland"),
    ("Hill", "Hill"), ("Mountain", "Mountain"), ("Swamp", "Swamp"),
    ("Underground", "Underground"), ("Underwater", "Underwater"), ("Urban", "Urban")])
    descrip = TextAreaField("Description", [validators.Length(min=1, max=5000)])
    public = BooleanField("Make public?")

    class Meta:
        csrf = False

class SearchEnviroForm(FlaskForm):
    name = StringField("Search by Name", [validators.Length(min=1, max=25)])
    etype = SelectField("Seach by Type", choices=[("Arctic", "Arctic"), ("Coastal", "Coastal"),
    ("Desert", "Desert"), ("Forest", "Forest"), ("Grassland", "Grassland"),
    ("Hill", "Hill"), ("Mountain", "Mountain"), ("Swamp", "Swamp"),
    ("Underground", "Underground"), ("Underwater", "Underwater"), ("Urban", "Urban")])
    owner = StringField("Search by Creator", [validators.Length(min=1, max=20)])
    whose = SelectField("Show own/public", choices=[(0, "All"), (1, "Own"), (2, "Others")])

    class Meta:
        csrf = False
