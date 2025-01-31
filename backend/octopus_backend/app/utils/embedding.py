from backend.octopus_backend.app.utils.vector_store import vector_store
import logging

def chunk_text(text, size=512):
    return [text[i:i+size] for i in range(0, len(text), size)]

def embed_and_store(user_id, note_id, chunks):
    for chunk in chunks:
        logging.info(f"Storing chunk: {chunk[:80]}...(User {user_id}, Note {note_id})")
        vector_store.add_texts(
            texts=[chunk],
            metadatas=[{"user_id": user_id, "note_id": note_id}]
        )