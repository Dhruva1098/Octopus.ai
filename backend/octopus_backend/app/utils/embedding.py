from backend.octopus_backend.app.utils.vector_store import vector_store


def chunk_text(text, size=512):
    return [text[i:i+size] for i in range(0, len(text), size)]

def embed_and_store(user_id, chunks):
    for chunk in chunks:
        vector_store.add_texts(
            texts=[chunk],
            metadata=[{"user_id": user_id}]
        )