from flask import request, Blueprint,jsonify

from backend.octopus_backend.app.models import note
from backend.octopus_backend.app.models.note import Note
from backend.octopus_backend.app.utils.db import db
from backend.octopus_backend.app.utils.neo4j import create_embeddings_and_relationships

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    user_id = data.get('user_id')
    content = data.get('content')

    notes = Note(content=content, user_id=user_id)
    db.session.add(notes)
    db.session.commit()

    create_embeddings_and_relationships(notes.id, content, user_id)

    return jsonify({'note_id': notes.id})

@notes_bp.route('/notes/<int:user_id>', methods=['GET'])
def get_notes(user_id):
    notes = Note.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': n.id, 'content':n.content} for n in notes])

