# Usage 
"""
curl -X POST http://127.0.0.1:5000/search_conferences -H "Content-Type: application/json" -d '{
  "location": "New York",
  "topics": ["AI", "Machine Learning"],
  "name": "AI Conference",
  "start_date": "2024-08-01T00:00:00Z",
  "end_date": "2024-08-10T23:59:59Z",
  "max_duration_hours": 12
}'
"""

from flask import request, jsonify, Blueprint
from datetime import datetime, timezone
import storage

search_bp = Blueprint('search', __name__)
@search_bp.route('/search_conferences', methods=['POST'])
def search_conferences():
    data = request.get_json()

    # Optional search parameters
    location = data.get('location', '')
    topics = data.get('topics', [])
    name = data.get('name', '')
    start_date = data.get('start_date', '')
    end_date = data.get('end_date', '')
    max_duration_hours = data.get('max_duration_hours', None)

    results = []
    
    for conf_name, conf_details in storage.conferences.items():
        matches = True
        
        if location and location.lower() not in conf_details['location'].lower():
            matches = False
        
        if name and name.lower() not in conf_details['name'].lower():
            matches = False

        if topics:
            conference_topics = set(conf_details['topics'])
            search_topics = set(topic.strip().lower() for topic in topics)
            if not search_topics.issubset(conference_topics):
                matches = False

        if start_date or end_date:
            conf_start = datetime.strptime(conf_details['start_timestamp'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            conf_end = datetime.strptime(conf_details['end_timestamp'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                if conf_end < start_date:
                    matches = False
            
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
                if conf_start > end_date:
                    matches = False

        if max_duration_hours is not None:
            duration_hours = (conf_end - conf_start).total_seconds() / 3600
            if duration_hours > max_duration_hours:
                matches = False
        
        if matches:
            results.append({
                'name': conf_details['name'],
                'location': conf_details['location'],
                'topics': conf_details['topics'],
                'start_timestamp': conf_details['start_timestamp'],
                'end_timestamp': conf_details['end_timestamp'],
                'available_slots': conf_details['available_slots']
            })

    return jsonify(results), 200
