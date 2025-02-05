import uuid

from flask import jsonify, request, Blueprint
from backend.octopus_backend.app.models.models import Users, Note
from backend.octopus_backend.app.utils.db import db
from backend.octopus_backend.app.utils.embedding import chunk_text
from backend.octopus_backend.app.utils.vector_store import vector_store, embeddings
from backend.octopus_backend.app.utils.vector_store import embeddings

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
    if not note_id:
        return jsonify({"error": "Note ID is required"}), 400

    try:
        # Step 1: Save or update the note in the relational database
        note = save_to_database(user_id, note_id, title, content)

        # Step 2: Delete old embeddings from AstraDB
        delete_old_embeddings_from_astradb(note_id)

        # Step 3: Store new embeddings in AstraDB
        store_new_embeddings_in_astradb(user_id, note_id, title, content, note.created_at)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500

    return jsonify({
        "message": "Note saved successfully",
        "note": {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.isoformat()
        }
    }), 201 if not Note.query.filter_by(id=note_id).first() else 200

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

    try:
        # Step 1: Delete the note from the relational database
        deleted_note = delete_from_database(user_id, note_id)

        # Step 2: Find embeddings in AstraDB
        ids_to_delete = find_embeddings_in_astradb(note_id)

        # Step 3: Delete embeddings from AstraDB
        delete_embeddings_from_astradb(ids_to_delete)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500

    return jsonify({
        "message": "Note deleted successfully",
        "deleted_note": {
            "id": deleted_note.id,
            "title": deleted_note.title,
            "content": deleted_note.content,
            "created_at": deleted_note.created_at.isoformat()
        }
    }), 200

def find_embeddings_in_astradb(note_id):
    """
    Find all embeddings in AstraDB for a given note_id.
    """
    try:
        results = vector_store.search(
            query="dummy_query",  # Dummy query (required by the API)
            search_type="similarity",  # Search type
            filter={"note_id": note_id},  # Filter by metadata
            limit=100  # Adjust the limit based on expected number of chunks
        )

        print("Results:", results)  # Debugging statement

        # Extract the AstraDB IDs from the results
        ids_to_delete = [result.id for result in results]
        print(f"Found {len(ids_to_delete)} embeddings for note_id={note_id}")

        return ids_to_delete

    except Exception as e:
        raise RuntimeError(f"Failed to find embeddings in AstraDB: {str(e)}")

def delete_from_database(user_id, note_id):
    """
    Delete a note from the relational database.
    """
    note = Note.query.filter_by(user_id=user_id, id=note_id).first()
    if not note:
        raise ValueError("Note not found")
    db.session.delete(note)
    db.session.commit()
    return note

def delete_embeddings_from_astradb(ids_to_delete):
    """
    Delete embeddings from AstraDB based on their IDs.
    """
    try:
        if ids_to_delete:
            vector_store.delete(ids=ids_to_delete)
        print(f"Deleted {len(ids_to_delete)} embeddings from AstraDB")

    except Exception as e:
        raise RuntimeError(f"Failed to delete embeddings from AstraDB: {str(e)}")

def save_to_database(user_id, note_id, title, content):
    """
    Save or update a note in the relational database.
    """
    note = Note.query.filter_by(id=note_id).first()

    if note:
        # Update existing note
        note.title = title
        note.content = content
        db.session.commit()
        print(f"Updated note with note_id={note_id}")
    else:
        # Create new note
        user = Users.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        note = Note(id=note_id, title=title, content=content, user=user)
        db.session.add(note)
        db.session.commit()
        print(f"Created new note with note_id={note_id}")

    return note

def delete_old_embeddings_from_astradb(note_id):
    """
    Delete old embeddings from AstraDB for a given note_id.
    """
    try:
        results = vector_store.search(
            query="dummy_query",  # Dummy query (required by the API)
            search_type="similarity",  # Search type
            filter={"note_id": note_id},  # Filter by metadata
            limit=100  # Adjust the limit based on expected number of chunks
        )

        print("Old embeddings:", results)  # Debugging statement

        # Extract the AstraDB IDs from the results
        ids_to_delete = [result.id for result in results]
        print(f"Found {len(ids_to_delete)} old embeddings for note_id={note_id}")

        if ids_to_delete:
            vector_store.delete(ids=ids_to_delete)
            print(f"Deleted {len(ids_to_delete)} old embeddings from AstraDB")

    except Exception as e:
        raise RuntimeError(f"Failed to delete old embeddings from AstraDB: {str(e)}")

def store_new_embeddings_in_astradb(user_id, note_id, title, content, created_at):
    """
    Embed and store new content in AstraDB using the add_texts method.
    """
    try:
        chunks = chunk_text(title, content)  # Chunk the text
        embedding = [embeddings.embed_query(chunk) for chunk in chunks]  # Generate embeddings

        # Prepare metadata for each chunk
        metadata = [{
            "note_id": note_id,
            "title": title,
            "content": chunk,
            "user_id": user_id,
            "created_at": created_at.isoformat()
        } for chunk in chunks]

        # Use the add_texts method to store embeddings in AstraDB
        vector_store.add_texts(
            texts=chunks,         # The text chunks
            embeddings=embedding,  # The corresponding embeddings
            metadatas=metadata  # Metadata for each chunk
        )
        print(f"Stored {len(chunks)} new embeddings for note_id={note_id}")

    except Exception as e:
        raise RuntimeError(f"Failed to store new embeddings in AstraDB: {str(e)}")
