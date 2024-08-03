# Dictionary storing conference details.
# Attributes: 'name', 'location', 'topics', 'start_timestamp', 'end_timestamp', 'available_slots'
conferences = {}

# Dictionary storing user details.
# Attributes: 'user_id', 'interested_topics'
users = {}

# Dictionary storing booking details.
# Attributes: 'booking_id', 'conference_name', 'user_id', 'confirmed'
bookings = {}

# Dictionary storing waitlist details for conferences.
# Attributes: 'conference_name', 'list' (user IDs waiting for a slot)
waitlists = {}

# Dictionary storing pending confirmation details for bookings.
# Attributes: 'booking_id', 'confirmation_time'
pending_confirmations = {}
