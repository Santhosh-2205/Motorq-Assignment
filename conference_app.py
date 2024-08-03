# Usage : To create new conference
"""
curl -X POST http://127.0.0.1:5000/add_conference \
-H "Content-Type: application/json" \
-d '{
  "name": "AI Conference 2024",
  "location": "New York",
  "topics": ["AI", "Machine Learning", "Deep Learning"],
  "start_timestamp": "2024-08-03T09:00:00Z",
  "end_timestamp": "2024-08-03T21:00:00Z",
  "available_slots": 100
}'
"""

from flask import request, jsonify, Blueprint
from datetime import datetime, timedelta
import storage

def is_alphanumeric_with_spaces(s):
    return s.replace(" ", "").isalnum()

conference_bp = Blueprint('conference_app', __name__)
@conference_bp.route('/add_conference', methods=['POST'])
def add_conference():
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'location', 'topics', 'start_timestamp', 'end_timestamp', 'available_slots']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Validation
    
    name = data['name']
    if not is_alphanumeric_with_spaces(name):
        return jsonify({"error": "Name can only contain alphanumeric characters and spaces"}), 400
    if name in storage.conferences:
        return jsonify({"error": "Conference name must be unique"}), 400

    location = data['location']
    if not is_alphanumeric_with_spaces(location):
        return jsonify({"error": "Location can only contain alphanumeric characters and spaces"}), 400

    topics = data['topics']
    if not isinstance(topics, list) or len(topics) > 10:
        return jsonify({"error": "Topics must be a list with a maximum of 10 strings"}), 400
    for topic in topics:
        if not is_alphanumeric_with_spaces(topic):
            return jsonify({"error": "Each topic can only contain alphanumeric characters and spaces"}), 400

    try:
        start_timestamp = datetime.strptime(data['start_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        end_timestamp = datetime.strptime(data['end_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return jsonify({"error": "Timestamps must be in the format 'YYYY-MM-DDTHH:MM:SSZ'"}), 400

    if start_timestamp >= end_timestamp:
        return jsonify({"error": "Start timestamp must be before end timestamp"}), 400
    if (end_timestamp - start_timestamp) > timedelta(hours=12):
        return jsonify({"error": "Duration should not exceed 12 hours"}), 400

    available_slots = data['available_slots']
    if not isinstance(available_slots, int) or available_slots <= 0:
        return jsonify({"error": "Available slots must be an integer greater than 0"}), 400

    # Add conference to storage
    storage.conferences[name] = {
        'name': name,
        'location': location,
        'topics': topics,
        'start_timestamp': start_timestamp.isoformat() + 'Z',
        'end_timestamp': end_timestamp.isoformat() + 'Z',
        'available_slots': available_slots
    }

    return jsonify({"message": "Conference added successfully"}), 201


