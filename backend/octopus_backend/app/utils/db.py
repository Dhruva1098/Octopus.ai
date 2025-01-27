from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aanshu007@@localhost:5432/octopus_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)