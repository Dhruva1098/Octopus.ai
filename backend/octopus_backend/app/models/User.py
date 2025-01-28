from backend.octopus_backend.app.utils.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.notes = []
