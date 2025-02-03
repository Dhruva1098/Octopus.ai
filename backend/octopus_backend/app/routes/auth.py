from flask import Blueprint, jsonify, request
from backend.octopus_backend.app.models.models import Users, db

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username and password."}), 400

    if Users.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    new_user = Users(username=username)
    if password:
        new_user.password = password

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User successfully registered.",
        "username": new_user.username,
        "id": new_user.id}), 201