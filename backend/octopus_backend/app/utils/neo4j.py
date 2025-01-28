from langchain_neo4j import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.llms import Ollama
from langchain_core.documents import Document
import os

llm = Ollama(model="llama2")
llm_transformer = LLMGraphTransformer(llm=llm)
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "password"

graph = Neo4jGraph()

def create_embeddings_and_relationships(note_id, content):

    documents = [Document(page_content=content)]
    graph_documents = llm_transformer.convert_to_graph_documents(documents)

    graph.add_graph_documents(graph_documents)