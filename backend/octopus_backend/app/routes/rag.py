from flask import Blueprint, request, jsonify
from langchain.chains import RetrievalQA
from langchain.llms import HiggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCasualLM

rag_bp = Blueprint('rag', __name__)

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCasualLM.from_pretrained("gpt2")
llm = HiggingFacePipeline(pipeline = "text-generation", model = model, tokenizer = tokenizer)

@rag_bp.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    user_id = data.get('user_id')

    query = """
    MATCH (n:Note)<-[:HAS_NOTE]-(u:User {id: $user_id})
    RETURN n.content AS content
    """
    results = neo4j.run(query, user_id = user_id).data
    context = " ".join([result['content'] for result in results])

    #answer
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=context)
    answer = qa_chain.run(question)

    return jsonify({'answer': answer})