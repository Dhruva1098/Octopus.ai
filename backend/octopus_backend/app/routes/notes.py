
from flask import jsonify, request, Blueprint
from backend.octopus_backend.app.models.models import Users, Note
from backend.octopus_backend.app.utils.db import db
from backend.octopus_backend.app.utils.embedding import chunk_text, embed_and_store
from backend.octopus_backend.app.utils.vector_store import vector_store

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/all_notes', methods=['POST'])
def get_all_notes():
    data = request.json
    user_id = data['user_id']
    if not user_id:
        return jsonify({"error": "No user id provided"}), 400
    notes = Note.query.filter_by(user_id=user_id).all()
    notes_data = [{"id": note.id, "content": note.content, "title":note.title, "created_at": note.created_at} for note in notes]
    return jsonify({"notes": notes_data}), 200

@notes_bp.route('/note_by_id/<int:note_id>', methods=['POST'])
def get_note_by_id(note_id):
    data = request.json
    user_id = data['user_id']
    note = Note.query.filter_by(user_id=user_id).filter_by(id=note_id).first()
    if not note:
        return jsonify({"error": "Note not found"}), 404
    return jsonify({"id": note.id,
                    "content":note.content,
                    "title":note.title}), 200

@notes_bp.route('/notes/delete', methods=['POST'])
def delete_note():
    data = request.json
    user_id = data.get('user_id')
    note_id = data.get('note_id')

    # Validate input
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    if not note_id:
        return jsonify({"error": "Note ID is required"}), 400

    # Find the note in the relational database
    note = Note.query.filter_by(user_id=user_id, id=note_id).first()
    if not note:
        return jsonify({"error": "Note not found"}), 404

    # Delete the note from the relational database
    db.session.delete(note)
    db.session.commit()

    # Search AstraDB for entries with the given note_id in metadata
    try:
        results = vector_store.search(
            query=[0] * 384,  # Dummy query (adjust dimensions if needed)
            search_type="similarity",  # Dummy search type
            filter={"note_id": note_id},  # Filter by metadata
            limit=100  # Adjust the limit based on expected number of chunks
        )

        print("Results:", results)  # Debugging statement

        # Extract the AstraDB IDs from the results
        ids_to_delete = []
        if isinstance(results[0], dict):  # Check if results are dictionaries
            ids_to_delete = [result["id"] for result in results]
        else:  # Assume results are objects
            ids_to_delete = [result.id for result in results]

        # Delete the entries from AstraDB
        if ids_to_delete:
            vector_store.delete(ids=ids_to_delete)

    except Exception as e:
        return jsonify({"error": "Failed to delete embeddings from AstraDB", "details": str(e)}), 500

    return jsonify({"message": "Note deleted successfully"}), 200


@notes_bp.route('/notes', methods=['POST'])
def create_or_update_note():
    data = request.json

    # Validate required fields
    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')
    note_id = data.get('note_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    if not title:
        return jsonify({"error": "Title is required"}), 400
    if not content:
        return jsonify({"error": "Content is required"}), 400

    # Check if the user exists
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if the note already exists
    note = Note.query.filter_by(id=note_id).first()

    if note:
        # Update the existing note
        note.title = title
        note.content = content
        db.session.commit()

        # Delete old embeddings from AstraDB
        try:
            results = vector_store.search(
                query=[0] * 384,  # Dummy query
                search_type="similarity",  # Dummy search type
                filter={"note_id": note_id},  # Filter by metadata
                limit=100  # Adjust the limit based on expected number of chunks
            )

            print("Results:", results)  # Debugging statement

            # Extract the AstraDB IDs from the results
            if isinstance(results[0], dict):  # Check if results are dictionaries
                ids_to_delete = [result["id"] for result in results]
            else:  # Assume results are objects
                ids_to_delete = [result.id for result in results]

            if ids_to_delete:
                vector_store.delete(ids=ids_to_delete)

        except Exception as e:
            return jsonify({"error": "Failed to delete old embeddings from AstraDB", "details": str(e)}), 500

        # Re-embed and store updated content
        chunks = chunk_text(title, content)
        embed_and_store(user.id, note.id, title, chunks, note.created_at)

        return jsonify({"message": "Note updated successfully"}), 200

    else:
        # Create a new note
        note = Note(id=note_id, title=title, content=content, user=user)
        db.session.add(note)
        db.session.commit()

        # Embed and store the new note
        chunks = chunk_text(title, content)
        embed_and_store(user.id, note.id, title, chunks, note.created_at)

        return jsonify({"message": "Note created successfully"}), 201