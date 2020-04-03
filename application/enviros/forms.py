from flask_wtf import FlaskForm
from wtforms import StringField, validators, TextAreaField, SelectField, BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from application.monsters.models import Monster

class EnviroForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, max=25)])
    etype = SelectField("Type", choices=[("Arctic", "Arctic"), ("Coastal", "Coastal"), ("Desert", "Desert"), ("Forest", "Forest"), ("Grassland", "Grassland"), ("Hill", "Hill"), ("Mountain", "Mountain"), ("Swamp", "Swamp"), ("Underground", "Underground"), ("Underwater", "Underwater"), ("Urban", "Urban")])
    descrip = TextAreaField("Description", [validators.Length(min=1, max=5000)])
    public = BooleanField("Make public?")

    class Meta:
        csrf = False

class EditEnviroForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, max=25)])
    etype = SelectField("Type", choices=[("Arctic", "Arctic"), ("Coastal", "Coastal"), ("Desert", "Desert"), ("Forest", "Forest"), ("Grassland", "Grassland"), ("Hill", "Hill"), ("Mountain", "Mountain"), ("Swamp", "Swamp"), ("Underground", "Underground"), ("Underwater", "Underwater"), ("Urban", "Urban")])
    descrip = TextAreaField("Description", [validators.Length(min=1, max=5000)])
    public = BooleanField("Make public?")

    class Meta:
        csrf = False

class AddMonsterForm(FlaskForm):
    mon = QuerySelectField(u'Monster', query_factory=Monster.get_monster_list, get_label='name', allow_blank=False)

    class Meta:
        csrf = False
