from backend.octopus_backend.app.utils.llm import model
from backend.octopus_backend.app.utils.vector_store import vector_store


def search_and_generate(user_id, query):
    chunks = vector_store.similarity_search(
        query=query,
        k=5,
        filter={"userId": user_id}
    )
    context = " ".join([c.page_content for c in chunks])

    prompt = f"Answer based on context: {context}\nQuestion: {query}"
    response = model.generate_content(prompt)
    return response.text
