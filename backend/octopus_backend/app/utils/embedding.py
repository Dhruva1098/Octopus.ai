from backend.octopus_backend.app.utils.vector_store import vector_store
import logging


def chunk_text(title, text, size=200, overlap=50):
    full_text = f"{title}\n{text}"
    chunks = []
    for i in range(0, len(full_text), size - overlap):
        chunks.append(full_text[i:i + size])
    return chunks

def embed_and_store(user_id, note_id, title, chunks, created_at):
    print(chunks)
    for chunk in chunks:
        logging.info(f"Storing chunk: {chunk[:80]}...(User {user_id}, Note {note_id})")
        vector_store.add_texts(
            texts=[chunk],
            metadatas=[{"user_id": user_id,
                        "note_id": note_id,
                        "title": title,
                        "date": created_at.strftime("%Y-%m-%d")}],
        )