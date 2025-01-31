from backend.octopus_backend.app.utils.llm import model
from backend.octopus_backend.app.utils.vector_store import vector_store, embeddings
import logging

def search_and_generate(user_id, query):
    query_embedding = embeddings.embed_query(query)
    chunks = vector_store.similarity_search_by_vector(
        embedding=query_embedding,
        k=5,
        filter={"user_id": user_id}
    )
    logging.info(f"Retrieved {len(chunks)} chunks")
    context = []
    note_ids = set()
    for chunk in chunks:
        context.append(chunk.page_content)
        note_ids.add(chunk.metadata.get("note_id"))

    context = " ".join(context)
    if not context:
        context = "No relevant context found."

    prompt = f"Answer based on context, do not answer from anything else, Text must only include the answer: {context}\nQuestion: {query}"
    response = model.generate_content(prompt)
    return {
        "answer": response.text.strip(),
        "note_ids": list(note_ids)

    }
