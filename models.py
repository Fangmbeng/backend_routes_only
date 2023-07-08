import base64
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import uuid
import secrets


login= LoginManager()
db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    chart=db.relationship('Chart', backref='chart',  lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique=True)
    avatar = db.Column(db.String(200))
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
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def get_avata(self):
        if self.avatar:
            return base64.b64encode(self.avatar).decode('utf-8')
        return None 

    
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
            "avatar": self.avatar,
            "post": [p.to_dict() for p in self.posts.all()],
            "chart": [c.to_dict() for c in self.chart.all()]
        }
        
    def get_user_id(self):
        return self.id
        
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

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img=db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # SQL Equivalent - FOREIGN KEY(user_id) REFERENCES user(id)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Post {self.id} | {self.brand}>"

    # Update method for the Post object
    def update(self, **kwargs):
        # for each key value that comes in as a keyword
        for key, value in kwargs.items():
            # if the key is an acceptable
            if key in {'brand', 'name','size', 'price', 'img'}:
                setattr(self, key, value)
        # Save the updates to the database
        db.session.commit()
        
    def set_id(self):
        return (secrets.token_urlsafe())
    
    def get_image_data(self):
        if self.img:
            return base64.b64encode(self.img).decode('utf-8')
        return None 

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def to_dict(self):
        return{
            "id":self.id,
            "brand": self.brand,
            'name':self.name,
            "size": self.size,
            'price':self.price,
            'img':self.img,
            "date_created": self.date_created,
            "user_id": self.user_id
        }
        
        
class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img=db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Post {self.id} | {self.name}>"

    # Update method for the Post object
    def update(self, **kwargs):
        # for each key value that comes in as a keyword
        for key, value in kwargs.items():
            # if the key is an acceptable
            if key in {'name', 'size', 'price', 'img'}:
                setattr(self, key, value)
        # Save the updates to the database
        db.session.commit()
        
    def set_id(self):
        return (secrets.token_urlsafe())
    
    def get_image_data(self):
        if self.img:
            return base64.b64encode(self.img).decode('utf-8')
        return None 

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def to_dict(self):
        return{
            "id":self.id,
            "name": self.name,
            "size": self.size,
            'price':self.price,
            'img':self.img,
            "user_id": self.user_id
        }