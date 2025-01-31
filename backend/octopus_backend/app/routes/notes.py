
from flask import jsonify, request, Blueprint
from backend.octopus_backend.app.models.models import User, Note
from backend.octopus_backend.app.utils.db import db
from backend.octopus_backend.app.utils.embedding import chunk_text, embed_and_store

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    user = User.query.get(data['user_id'])
    note = Note(content=data['content'], user=user)
    db.session.add(note)
    db.session.commit()

    chunks = chunk_text(note.content)
    embed_and_store(user.id, note.id, chunks)
    return jsonify({"message": "Note created"}), 201

