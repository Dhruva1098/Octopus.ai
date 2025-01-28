from flask import Flask
from backend.octopus_backend.app.utils.db import init_db, db
from backend.octopus_backend.app.routes import notes, rag, auth
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aanshu007@@localhost:5432/octopus_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth.auth_bp, url_prefix='/api')
    app.register_blueprint(notes.notes_bp, url_prefix='/api')
    app.register_blueprint(rag.rag_bp, url_prefix='/api')

    return app