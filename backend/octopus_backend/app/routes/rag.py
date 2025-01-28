from flask import request, jsonify, Blueprint
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_community.llms import Ollama
from backend.octopus_backend.app.utils.neo4j import graph

rag_bp = Blueprint('rag', __name__)

llm = Ollama(model="llama2")
enhanced_graph = Neo4jGraph(enhanced_schema=True)
chain = GraphCypherQAChain.from_llm(graph=enhanced_graph, llm=llm, verbose=True, allow_dangerous_requests=True)

@rag_bp.route('/ask', methods=["POST"])
def ask_question():
    data = request.json
    question = data['question']
    user_id = data['user_id']
    response = chain.invoke({"query": question})

    return jsonify(response)