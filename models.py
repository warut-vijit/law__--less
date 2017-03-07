from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Extension(db.Model):
    __tablename__ = 'extensions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(120))
    rating_points = db.Column(db.Integer)
    total_ratings = db.Column(db.Integer)