# Usage
"""
curl -X POST http://127.0.0.1:5000/confirm_waitlist_booking -H "Content-Type: application/json" -d '{
  "booking_id": "booking-id"
}'
"""

from flask import request, jsonify, Blueprint
from datetime import datetime, timedelta, timezone
import storage

confirm_bp = Blueprint('confirm_app', __name__)
@confirm_bp.route('/confirm_waitlist_booking', methods=['POST'])
def confirm_waitlist_booking():
    data = request.get_json()

    # Validate required fields
    required_fields = ['booking_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    booking_id = data['booking_id']

    if booking_id not in storage.bookings or booking_id not in storage.pending_confirmations:
        return jsonify({"error": "Booking ID does not exist or not eligible for confirmation"}), 400

    conference_name = storage.bookings[booking_id]['conference_name']
    
    confirmation_time = storage.pending_confirmations[booking_id]
    if datetime.now(timezone.utc) > confirmation_time + timedelta(hours=1):
        # Move user to the end of the waitlist
        user_id = storage.bookings[booking_id]['user_id']
        storage.waitlists[conference_name].append({'user_id': user_id, 'booking_id': booking_id})
        del storage.pending_confirmations[booking_id]
        return jsonify({"error": "Confirmation time expired, wait for your turn again"}), 400

    # Confirm the booking
    storage.bookings[booking_id]['confirmed'] = True
    del storage.pending_confirmations[booking_id]
    storage.conferences[conference_name]['available_slots'] -= 1

    return jsonify({"message": "Waitlist booking confirmed", "booking_id": booking_id}), 200


