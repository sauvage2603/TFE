from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(1000))
    admin= db.Column(db.String(1))
    ticket = db.relationship('Ticket',backref='user')

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sujet = db.Column(db.String(30), nullable=False)
    objet = db.Column(db.String(1000), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    admin=db.Column(db.String(100))
    etat=db.Column(db.String(20),nullable=False)
    id_reponse = db.relationship('Reponse', backref='ticket')

    def __init__(self, sujet,objet,user_id,admin,etat):
      self.sujet = sujet
      self.objet = objet
      self.user_id = user_id
      self.admin = admin
      self.etat=etat

class Reponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reponse= db.Column(db.String(1000), nullable=False)
    user = db.Column(db.String(1000),nullable=False)
    id_reponse=db.Column(db.Integer, db.ForeignKey('ticket.id'),nullable=False)

    def __init__(self,reponse,user,id_reponse):
        self.reponse = reponse
        self.user = user
        self.id_reponse = id_reponse