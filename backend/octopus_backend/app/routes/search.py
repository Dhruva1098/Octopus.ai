from flask import request, jsonify, Blueprint

from backend.octopus_backend.app.utils.rag import search_and_generate


search_bp = Blueprint('search', __name__)
@search_bp.route('/ask', methods=['POST'])
def search():
    data = request.json
    user_id = int(data['user_id'])
    query = data['query']

    if not query:
        return jsonify({"error":"Query is empty"}), 400

    answer = search_and_generate(user_id, query)
    return jsonify({
        "answer": answer["answer"],
        "note_ids": answer["note_ids"]
    }), 200