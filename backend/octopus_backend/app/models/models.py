
from backend.octopus_backend.app.utils.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    notes = db.relationship('Note', backref='user')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.Colomn(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())