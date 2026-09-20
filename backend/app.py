import os
import sys

# Ensure backend directory is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from routes.patients import patients_bp
from routes.doctors import doctors_bp
from routes.appointments import appointments_bp

def create_app():
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Enable CORS for all origins

    # Register Blueprints
    app.register_blueprint(patients_bp)
    app.register_blueprint(doctors_bp)
    app.register_blueprint(appointments_bp)

    @app.route('/')
    def index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/health', methods=['GET'])
    def health_check():
        """Healthcheck endpoint for monitoring & DevOps probing"""
        return jsonify({
            "status": "ok",
            "service": "HealthPulse Backend API",
            "version": "1.0.0"
        }), 200


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    print(f"Starting HealthPulse Flask Server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
