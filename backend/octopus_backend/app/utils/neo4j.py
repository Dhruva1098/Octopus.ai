from py2neo import Graph
from langchain_huggingface import HuggingFaceEmbeddings

embedder = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
neo4j_graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

def create_embeddings_and_relationships(note_id, content, user_id):

    embedding = embedder.embed_sentence(content)

    query = """
    MERGE (c:Concept {id: $note_id})
    SET c.embedding = $embedding, c.content = $content
    WITH c
    MATCH (u:User {id: $user_id})
    MERGE (u)-[:HAS_CONCEPT]->(c)
    """
    neo4j_graph.run(query, note_id = note_id, embedding = embedding, content = content, user_id = user_id)