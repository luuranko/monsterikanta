from application import db
from application.models import Base

class Enviro(Base):

    name = db.Column(db.String(144), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    etype = db.Column(db.String(200), nullable=False)
    descrip = db.Column(db.String(1000), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    account_name = db.Column(db.String(144), nullable=False)

    def __init__(self, name, etype, descrip):
        self.name = name
        self.etype = etype
        self.descrip = descrip
