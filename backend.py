from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import random  # Simulate detection results

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///detections.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db = SQLAlchemy(app)

# Database model for storing detection history
class Detection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    detection_time = db.Column(db.DateTime, default=datetime.utcnow)
    fake_percentage = db.Column(db.Integer, nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Simulate fake percentage detection
    fake_percentage = random.randint(0, 100)

    # Save detection to database
    detection = Detection(file_name=filename, fake_percentage=fake_percentage)
    db.session.add(detection)
    db.session.commit()

    return jsonify({
        "file_name": filename,
        "fake_percentage": fake_percentage
    })

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
