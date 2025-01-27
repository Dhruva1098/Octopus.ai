from py2neo import Graph

neo4j = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

def create_note_node(note_id, content):
    query = """
    CREATE (n:Note {{id: {note_id}, content: "{content}"}})
    """
    neo4j_graph.run(query, note_id = note_id, content = content)