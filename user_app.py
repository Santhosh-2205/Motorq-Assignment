# Usage : To create new user
"""
curl -X POST http://127.0.0.1:5000/add_user \
-H "Content-Type: application/json" \
-d '{
  "user_id": "user123",
  "interested_topics": ["AI", "Data Science", "Blockchain"]
}'
"""

from flask import request, jsonify, Blueprint
import storage

def is_alphanumeric_with_spaces(s):
    return s.replace(" ", "").isalnum()

def is_alphanumeric(s):
    return s.isalnum()

user_bp = Blueprint('user_app', __name__)
@user_bp.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()

    # Validate required fields
    required_fields = ['user_id', 'interested_topics']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Validation
    user_id = data['user_id']
    if not is_alphanumeric(user_id):
        return jsonify({"error": "UserID can only contain alphanumeric characters"}), 400
    if user_id in storage.users:
        return jsonify({"error": "UserID must be unique"}), 400

    interested_topics = data['interested_topics']
    if not isinstance(interested_topics, list) or len(interested_topics) > 50:
        return jsonify({"error": "Interested topics must be a list with a maximum of 50 strings"}), 400
    for topic in interested_topics:
        if not is_alphanumeric_with_spaces(topic):
            return jsonify({"error": "Each interested topic can only contain alphanumeric characters and spaces"}), 400

    # Add user to storage
    storage.users[user_id] = {
        'user_id': user_id,
        'interested_topics': interested_topics
    }

    return jsonify({"message": "User added successfully"}), 201
