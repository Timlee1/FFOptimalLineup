from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    league_setting = db.relationship('League', backref='author_user',lazy='dynamic')
    roster_setting = db.relationship('Roster', backref='author_user',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def user_league(self):
        return League.query.filter_by(user_id=self.id).first()
    
    def user_roster(self):
        return Roster.query.filter_by(user_id=self.id).first()
    
    def has_league(self):
         if League.query.filter_by(user_id=self.id).count() > 0:
             return True 
         return False

class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qb = db.Column(db.Integer)
    rb = db.Column(db.Integer)
    wr = db.Column(db.Integer)
    te = db.Column(db.Integer)
    rb_wr = db.Column(db.Integer)
    rb_te = db.Column(db.Integer)
    wr_te = db.Column(db.Integer)
    rb_wr_te = db.Column(db.Integer)
    qb_rb_wr_te = db.Column(db.Integer)
    dst = db.Column(db.Integer)
    k = db.Column(db.Integer)
    scoring = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    
    def __repr__(self):
        return '<League {}>'.format(self.qb)

class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    position = db.Column(db.String(64))
    team = db.Column(db.String(64))
    opponent = db.Column(db.String(64))
    roster_setting = db.relationship('Roster', backref='author_player',lazy='dynamic')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))