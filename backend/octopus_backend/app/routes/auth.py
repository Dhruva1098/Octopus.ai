from flask import Blueprint, jsonify, request
from backend.octopus_backend.app.utils.db import db
from backend.octopus_backend.app.models import User

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User(username=username, password = password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'user_id': user.id})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        return jsonify({'message': 'Invalid username or password'})

    return jsonify({'user_id': user.id})