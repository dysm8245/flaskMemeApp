from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, first_name, last_name, email, username, password):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = self.set_pwhash(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())
        
    def set_pwhash(self, password):
        return generate_password_hash(password)
        
    def set_token(self, length):
        return secrets.token_hex(length)
    
class Memes(db.Model):
    id = db.Column(db.String, primary_key=True)
    img_src = db.Column(db.String, nullable=False)

    def __init__(self, img_src):
        self.id = self.set_id()
        self.img_src = img_src

    def set_id(self):
        return str(uuid.uuid4())

class UserMemes(db.Model):
    id = db.Column(db.String, primary_key=True)
    caption = db.Column(db.String, nullable=False)
    img_src = db.Column(db.String, nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, img_src, caption, user_token):
        self.id = self.set_id()
        self.img_src = img_src
        self.caption = caption
        self.user_token = user_token
    
    def set_id(self):
        return str(uuid.uuid4())
    
class MemeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'caption', 'img_src', 'user_token']

class TemplateSchema(ma.Schema):
    class Meta:
        fields = ['id', 'img_src']

meme_schema = MemeSchema()
memes_schema = MemeSchema(many=True)

template_schema = TemplateSchema()
templates_schema = TemplateSchema(many=True)

