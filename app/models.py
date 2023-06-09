from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from time import time


class Users(UserMixin, db.Model):
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
    
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Users.query.get(id)

    def user_league(self):
        return League.query.filter_by(user_id=self.id).first()
    
    def user_roster(self):
        return Player.query.join(Roster, Player.id == Roster.player_id).filter_by(user_id=self.id)
    
    def has_league(self):
         if League.query.filter_by(user_id=self.id).count() > 0:
             return True 
         return False
    
    def is_player_on_user_roster(self, player_id):
        if Roster.query.filter_by(user_id=self.id).filter_by(player_id=player_id).count() > 0:
            return True 
        return False 
    
    def player_on_user_roster(self, player_id):
        return Roster.query.filter_by(user_id=self.id).filter_by(player_id=player_id)
    
    def user_opponent_roster(self):
        return Player.query.join(OpponentRoster, Player.id == OpponentRoster.player_id).filter_by(user_id=self.id)
    
    def is_player_on_user_opponent_roster(self, player_id):
        if OpponentRoster.query.filter_by(user_id=self.id).filter_by(player_id=player_id).count() > 0:
            return True 

    def player_on_user_opponent_roster(self, player_id):
        return OpponentRoster.query.filter_by(user_id=self.id).filter_by(player_id=player_id)

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
    kicker = db.Column(db.Integer)
    scoring = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    
    def __repr__(self):
        return '<League {}>'.format(self.qb)

class Roster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

class OpponentRoster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(64))
    pos = db.Column(db.String(64))
    team = db.Column(db.String(64))
    opponent = db.Column(db.String(64))
    home = db.Column(db.Boolean)
    proj_std = db.Column(db.Float)
    avg_rank_std = db.Column(db.Float)
    sdev_rank_std = db.Column(db.Float)
    proj_half = db.Column(db.Float)
    avg_rank_half = db.Column(db.Float)
    sdev_rank_half = db.Column(db.Float)
    proj_ppr = db.Column(db.Float)
    avg_rank_ppr = db.Column(db.Float)
    sdev_rank_ppr = db.Column(db.Float)
    roster_setting = db.relationship('Roster', backref='author_player',lazy='dynamic')

    def get_all_players():
        return Player.query.all()
    
@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


