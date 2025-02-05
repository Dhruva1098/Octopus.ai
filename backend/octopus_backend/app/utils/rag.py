import json
from datetime import datetime, timedelta
from typing import Any, Dict

from backend.octopus_backend.app.utils.llm import model
from backend.octopus_backend.app.utils.vector_store import vector_store, embeddings
import logging

def search_and_generate(user_id, query):
    filters = parse_natural_language_query(query)

    astra_filters = {"user_id": user_id}

    if filters["start_date"] or filters["end_date"]:
        astra_filters["date"] = {}
        if filters["start_date"]:
            astra_filters["date"]["$gte"] = filters["start_date"]
        if filters["end_date"]:
            astra_filters["date"]["$lte"] = filters["end_date"]

    if filters["topics"]:
        astra_filters["$or"] = [
            {"content": {"$contains": topic}} for topic in filters["topics"]
        ]
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


    if filters["intent"] == "summary":
        prompt= f"""
        Summarise the following context in concise and coherent summary:
        Context: {context}"""
    else:
        prompt = f"""
        Answer the following question based on the provided context. Do not use any external knowledge.
        Context: {context}
        Question: {query}
        Answer:"""
    response = model.generate_content(prompt)
    return {
        "answer": response.text.strip(),
        "note_ids": list(note_ids)
    }

def parse_natural_language_query(query: str) -> Dict[str, Any]:

    #Extract structured filters (dates, topics, summarization intent) from natural language queries.
    #returns a dict

    prompt = f"""
    Analyze the user's query and extract the following:
    - Intent: eg. is user asking for a summary or a summarization intent. return summary
    - Topics/keywords (e.g., "machine learning", "meeting notes")
    - Date range (relative like "last week" or absolute like "March 2024")
    Return ONLY a JSON object with keys: "intent", "topics", "start_date", "end_date".
    Query: {query}
    """
    response = model.generate_content(prompt)
    try:
        filters = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        logging.error(f"Failed to parse LLM response: {response.text}")
        return {"intent": None, "topics": [], "start_date": None, "end_date": None}

    # Convert relative dates to absolute dates
    if filters.get("start_date") in ["last week", "past week"]:
        filters["start_date"] = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    elif filters.get("start_date") == "last month":
        filters["start_date"] = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    return filters


"""
def hybrid_search(query, texts, embeddings, vector_store, top_k = 5):
    vectorizer = TfidfVectorizer()
    tdidf_matrix = vectorizer.fit_transform(texts)
    query_vector = vectorizer.transform([query])
    keyword_scores = (query_vector * tdidf_matrix).toarray()
    keyword_results = [texts[i] for i in keyword_scores.argsort()[-top_k:][::-1]]

    #sementic search
    query_embedding = embeddings.embed_query(query)
    semantic_results = vector_store.similarity_search_by_vector(
        embedding=query_embedding,
        k = top_k
    )
    semantic_texts = [results.page_content for results in semantic_results]

    combined_results = list(set(keyword_results + semantic_texts))
    return combined_results
"""