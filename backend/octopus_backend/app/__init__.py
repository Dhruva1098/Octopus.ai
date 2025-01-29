# __init__.py
import logging
from flask import Flask
from backend.octopus_backend.app.utils.db import db
from backend.octopus_backend.app.utils.vector_store import vector_store
from backend.octopus_backend.app.utils import llm


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Aanshu007%40@localhost:5432/octopus_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create database tables

    # Configure logging
    logging.basicConfig(level=logging.DEBUG if app.debug else logging.INFO)

    # Register API routes
    from backend.octopus_backend.app.routes.notes import notes_bp
    from backend.octopus_backend.app.routes.search import search_bp
    app.register_blueprint(notes_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')

    return app