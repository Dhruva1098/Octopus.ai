from flask import request, jsonify, Blueprint

from backend.octopus_backend.app.utils.rag import search_and_generate

search_bp = Blueprint('search', __name__)

@search_bp.route('/ask', methods=['POST'])
def search():
    data = request.json
    answer = search_and_generate(data['user_id'], data['query'])
    return jsonify({"answer": answer})