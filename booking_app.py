# Usage : To book for a conference
"""
curl -X POST http://127.0.0.1:5000/book_conference \
-H "Content-Type: application/json" \
-d '{
  "name": "ABC Conference 2024",
  "user_id": "user123"
}'
"""

from flask import request, jsonify, Blueprint
from datetime import datetime, timedelta
import storage
import uuid

booking_bp = Blueprint('booking_app', __name__)
@booking_bp.route('/book_conference', methods=['POST'])
def book_conference():
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    conference_name = data['name']
    user_id = data['user_id']

    # Validation
    if conference_name not in storage.conferences:
        return jsonify({"error": "Conference does not exist"}), 400

    if user_id not in storage.users:
        return jsonify({"error": "User does not exist"}), 400

    for booking_id, booking in storage.bookings.items():
        if booking['conference_name'] == conference_name and booking['user_id'] == user_id:
            status = "confirmed" if booking['confirmed'] else "waiting list"
            return jsonify({"error": f"User already registered for this conference with booking ID {booking_id}. Status: {status}"}), 400

    # Overlapping bookings
    start_time = datetime.strptime(storage.conferences[conference_name]['start_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.strptime(storage.conferences[conference_name]['end_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
    
    for booking in storage.bookings.values():
        if booking['user_id'] == user_id:
            existing_conference = storage.conferences[booking['conference_name']]
            existing_start = datetime.strptime(existing_conference['start_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
            existing_end = datetime.strptime(existing_conference['end_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
            if start_time < existing_end and end_time > existing_start:
                return jsonify({"error": "User has an overlapping booking"}), 400

    booking_id = str(uuid.uuid4())
    if storage.conferences[conference_name]['available_slots'] > 0:
        storage.bookings[booking_id] = {
            'conference_name': conference_name,
            'user_id': user_id,
            'confirmed': True
        }
        storage.conferences[conference_name]['available_slots'] -= 1
        return jsonify({"message": "Booking successful", "booking_id": booking_id}), 201
    else:
        storage.bookings[booking_id] = {
            'conference_name': conference_name,
            'user_id': user_id,
            'confirmed': False
        }
        if conference_name not in storage.waitlists:
            storage.waitlists[conference_name] = []
        storage.waitlists[conference_name].append({'user_id': user_id, 'booking_id': booking_id})
        return jsonify({"message": "Conference is fully booked, added to waitlist", "booking_id": booking_id}), 200