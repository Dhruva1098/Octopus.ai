from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = '-'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False