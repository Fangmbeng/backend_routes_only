import base64
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from sqlalchemy.ext.declarative import declarative_base


login= LoginManager()
db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avatar = db.Column(db.LargeBinary)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
    def update(self, **kwargs):
        # for each key value that comes in as a keyword
        for key, value in kwargs.items():
            username = {'username'}
            email = {'email'}
            password ={'password'}
            avatar={"avatar"}
            if key in username or email or password or avatar:
                setattr(self, key, value)
        # Save the updates to the database
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        return{
            "id":self.id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "date_created": self.date_created,
            "avatar": self.avatar
        }
        
    def get_user_id(self):
        return self.id
    
    def get_avatar(self):
        return self.avatar
        
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(minutes=1):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.commit()
        return self.token
    
    def revoke_token(self):
        now = datetime.utcnow()
        self.token_expiration = now - timedelta(seconds=1)
        db.session.commit()

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)