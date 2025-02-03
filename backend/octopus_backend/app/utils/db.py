from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aanshu007%40@localhost:5432/octopus_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False