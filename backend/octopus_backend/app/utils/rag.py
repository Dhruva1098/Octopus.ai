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

    prompt = f"Answer based on context, do not answer from anything else, Text must only include the answer: {context}\nQuestion: {query}"
    response = model.generate_content(prompt)
    return {
        "answer": response.text.strip(),
        "note_ids": list(note_ids)
    }

def parse_natural_language_query(query:str) -> Dict[str, Any]:
    """
    Extract structured filters (dates, topics) from natural language queries.
    Returns a filter dictionary compatible with Astra.
    """
    prompt = f"""
    Extract the following from the user's query:
    - Topic/keywords (e.g., "machine learning", "meeting notes")
    - Date range (relative like "last week" or absolute like "March 2024")

    Return ONLY a JSON object with keys: "topics", "start_date", "end_date".
    If no dates/topics are found, set values to null.

    Query: {query}
    """

    response = model.generate_content(prompt)
    try:
        filters = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        return {"topics": None, "start_date": None, "end_date": None}

    #need absolute dates
    if filters.get("start_date") in ["last week", "past week"]:
        filters["start_date"] = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    elif filters.get("start_date") == "last month":
        filters["start_date"] = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    return filters