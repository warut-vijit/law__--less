from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Extension(db.Model):
    __tablename__ = 'extensions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(120))
    description = db.Column(db.String(200))
    rating_points = db.Column(db.Integer)
    total_ratings = db.Column(db.Integer)
    code = db.Column(db.Text)
    field = db.Column(db.String(50)) # will be replaced with foreign key soon
    
    def get_dict(self):
        return {
            "id":self.id,
            "name":self.name, 
            "author":self.author, 
            "description":self.description,
            "rating_points":self.rating_points,
            "total_ratings":self.total_ratings,
            "field":self.field,
            "code":self.code
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(120))
    password_hash = db.Column(db.String(256))
    since = db.Column(db.DateTime)
    ends = db.Column(db.DateTime)
    documents = db.relationship('Document', backref='user', lazy='dynamic')

    def get_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "username":self.username,
            "password_hash":self.password_hash,
            "since":self.since,
            "ends":self.ends,
            "documents":self.documents.count()
        }

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))