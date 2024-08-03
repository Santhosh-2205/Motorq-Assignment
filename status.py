# Usage 
"""
curl -X POST http://127.0.0.1:5000/booking_status -H "Content-Type: application/json" -d '{
  "booking_id": "your-booking-id"
}'
"""

from flask import request, jsonify, Blueprint
from datetime import datetime, timedelta, timezone
import storage

status_bp = Blueprint('status', __name__)
@status_bp.route('/booking_status', methods=['POST'])
def booking_status():
    data = request.get_json()

    if 'booking_id' not in data:
        return jsonify({"error": "'booking_id' is required"}), 400

    booking_id = data['booking_id']

    if not booking_id:
        return jsonify({"error": "'booking_id' is required"}), 400

    if booking_id not in storage.bookings:
        return jsonify({"status": "Either booking cancelled or Booking ID is wrong"}), 404

    booking = storage.bookings[booking_id]

    if booking['confirmed']:
        return jsonify({"status": "Confirmed"}), 200
    else:
        if booking_id in storage.pending_confirmations:
            confirmation_time = storage.pending_confirmations[booking_id]
            current_time = datetime.now(timezone.utc)
            time_remaining = (confirmation_time + timedelta(hours=1)) - current_time
            if time_remaining > timedelta(0):
                return jsonify({
                    "status": "Waitlisted",
                    "can_confirm": True,
                    "confirm_by": (confirmation_time + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
                }), 200
            else:
                return jsonify({
                    "status": "Waitlisted",
                    "can_confirm": False,
                    "confirm_by": (confirmation_time + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
                }), 200
        else:
            return jsonify({"status": "Waitlisted", "can_confirm": False}), 200
