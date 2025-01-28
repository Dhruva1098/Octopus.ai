from flask import request, jsonify, Blueprint
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from backend.octopus_backend.app.utils.neo4j import embedder, neo4j_graph

rag_bp = Blueprint('rag', __name__)
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained("gpt2")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
llm = HuggingFacePipeline(pipeline=pipe)

@rag_bp.route('/ask', methods=["POST"])
def ask_question():
    data = request.json
    question = data['question']
    user_id = data['user_id']

    question_embedding = embedder.embed_query(question)

    query = """
    MATCH (u:User {id: $user_id})-[:HAS_CONCEPT]->(c:concept)
    RETURN c.content AS context
    """
    results = neo4j_graph.run(query,question_embedding=question_embedding, user_id=user_id).data()
    context = " ".join([result['context'] for result in results])

    qa_chain = RetrievalQA.from_chain_type(llm, retriever = context)
    answer = qa_chain.run(question)

    return jsonify({'answer':answer})