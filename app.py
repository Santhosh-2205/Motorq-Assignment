from flask import Flask
from conference_app import conference_bp
from user_app import user_bp
from booking_app import booking_bp
from cancel_booking import cancel_bp
from confirm_book import confirm_bp
from status import status_bp
from search import search_bp

app = Flask(__name__)
app.register_blueprint(conference_bp)
app.register_blueprint(user_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(cancel_bp)
app.register_blueprint(confirm_bp)
app.register_blueprint(status_bp)
app.register_blueprint(search_bp)

if __name__ == '__main__':
    app.run(debug=True)
