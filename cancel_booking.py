# Usage : To cancel a booking
"""
curl -X POST http://127.0.0.1:5000/cancel_booking \
-H "Content-Type: application/json" \
-d '{
  "booking_id": "939c25f9-07af-4dca-aa33-1147894a72c6."
}'
"""

from flask import request, jsonify, Blueprint
from datetime import datetime, timedelta, timezone
import storage
import uuid

cancel_bp = Blueprint('cancel_booking', __name__)
@cancel_bp.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    data = request.get_json()

    # Validate required fields
    required_fields = ['booking_id']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    booking_id = data['booking_id']

    if booking_id not in storage.bookings:
        return jsonify({"error": "Booking ID does not exist"}), 400

    booking = storage.bookings.pop(booking_id)

    if booking['confirmed']:
        storage.conferences[booking['conference_name']]['available_slots'] += 1

        if booking['conference_name'] in storage.waitlists and storage.waitlists[booking['conference_name']]:
            next_waitlist_entry = storage.waitlists[booking['conference_name']].pop(0)
            next_user_id = next_waitlist_entry['user_id']
            next_booking_id = next_waitlist_entry['booking_id']
            storage.pending_confirmations[next_booking_id] = datetime.now(timezone.utc)
    else:
        storage.waitlists[booking['conference_name']].remove(booking['user_id'])

    return jsonify({"message": "Booking cancelled successfully"}), 200
