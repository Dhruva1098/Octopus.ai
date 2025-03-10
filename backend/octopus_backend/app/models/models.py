
from backend.octopus_backend.app.utils.db import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(129), nullable=False)
    notes = db.relationship('Note', backref='user')

class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())