from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SelectField, BooleanField

class EnviroForm(FlaskForm):
    name = StringField("Name")
    etype = SelectField("Type", choices=[("Arctic", "Arctic"), ("Coastal", "Coastal"), ("Desert", "Desert"), ("Forest", "Forest"), ("Grassland", "Grassland"), ("Hill", "Hill"), ("Mountain", "Mountain"), ("Swamp", "Swamp"), ("Underground", "Underground"), ("Underwater", "Underwater"), ("Urban", "Urban")])
    descrip = TextAreaField("Description")
    public = BooleanField("Make public?")

    class Meta:
        csrf = False

class EditEnviroForm(FlaskForm):
    name = StringField("Name")
    etype = SelectField("Type", choices=[("Arctic", "Arctic"), ("Coastal", "Coastal"), ("Desert", "Desert"), ("Forest", "Forest"), ("Grassland", "Grassland"), ("Hill", "Hill"), ("Mountain", "Mountain"), ("Swamp", "Swamp"), ("Underground", "Underground"), ("Underwater", "Underwater"), ("Urban", "Urban")])
    descrip = TextAreaField("Description")
    public = BooleanField("Make public?")

    class Meta:
        csrf = False

