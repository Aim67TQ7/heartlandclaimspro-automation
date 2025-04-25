#!/usr/bin/env python3
"""
Photo Collection API

This module provides a Flask API for the mobile app that contractors use to submit
photos of storm damage. It handles photo uploads, metadata collection, and integration
with the AI damage assessment system.
"""

import os
import json
import uuid
import logging
from datetime import datetime
import argparse

# Flask for API
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("photo_api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("photo_api")

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'photo_uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'heic'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max upload size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper functions
def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_metadata(photo_id, metadata):
    """Save photo metadata to a JSON file."""
    metadata_dir = os.path.join(UPLOAD_FOLDER, 'metadata')
    os.makedirs(metadata_dir, exist_ok=True)
    
    metadata_file = os.path.join(metadata_dir, f"{photo_id}.json")
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Saved metadata for photo {photo_id}")
    return metadata_file

def get_contractor_jobs(contractor_id):
    """Get active jobs for a contractor."""
    # In a real implementation, this would query a database
    # For now, we'll return mock data
    return [
        {
            "job_id": "job-001",
            "address": "123 Main St, Anytown, USA",
            "storm_type": "Hurricane",
            "severity": "Severe",
            "status": "Assigned",
            "created_at": "2025-04-23T14:30:00Z",
            "instructions": "Take photos of roof, siding, and any water damage"
        },
        {
            "job_id": "job-002",
            "address": "456 Oak Ave, Somewhere, USA",
            "storm_type": "Tornado",
            "severity": "Extreme",
            "status": "In Progress",
            "created_at": "2025-04-24T09:15:00Z",
            "instructions": "Document all structural damage and debris"
        }
    ]

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/contractor/login', methods=['POST'])
def contractor_login():
    """Contractor login endpoint."""
    data = request.json
    
    # In a real implementation, this would validate credentials against a database
    # For now, we'll accept any login with an email and password
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password required"}), 400
    
    # Mock successful login
    contractor_id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    
    logger.info(f"Contractor login: {data['email']}")
    
    return jsonify({
        "contractor_id": contractor_id,
        "token": token,
        "name": "John Doe",
        "email": data['email'],
        "phone": "555-123-4567"
    })

@app.route('/api/contractor/jobs', methods=['GET'])
def get_jobs():
    """Get active jobs for a contractor."""
    # In a real implementation, this would validate the token
    # and retrieve jobs for the specific contractor
    contractor_id = request.headers.get('X-Contractor-ID')
    
    if not contractor_id:
        return jsonify({"error": "Contractor ID required"}), 400
    
    jobs = get_contractor_jobs(contractor_id)
    
    return jsonify({
        "contractor_id": contractor_id,
        "jobs": jobs
    })

@app.route('/api/photos/upload', methods=['POST'])
def upload_photo():
    """Upload a photo of storm damage."""
    # Check if contractor ID is provided
    contractor_id = request.headers.get('X-Contractor-ID')
    if not contractor_id:
        return jsonify({"error": "Contractor ID required"}), 400
    
    # Check if job ID is provided
    job_id = request.form.get('job_id')
    if not job_id:
        return jsonify({"error": "Job ID required"}), 400
    
    # Check if the post request has the file part
    if 'photo' not in request.files:
        return jsonify({"error": "No photo part"}), 400
    
    file = request.files['photo']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # Generate a unique ID for the photo
        photo_id = str(uuid.uuid4())
        
        # Create directory for this job if it doesn't exist
        job_dir = os.path.join(UPLOAD_FOLDER, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1].lower()
        save_path = os.path.join(job_dir, f"{photo_id}.{extension}")
        file.save(save_path)
        
        # Collect metadata
        metadata = {
            "photo_id": photo_id,
            "job_id": job_id,
            "contractor_id": contractor_id,
            "original_filename": filename,
            "file_size_bytes": os.path.getsize(save_path),
            "upload_time": datetime.now().isoformat(),
            "location": {
                "latitude": request.form.get('latitude'),
                "longitude": request.form.get('longitude'),
                "accuracy": request.form.get('accuracy')
            },
            "device_info": {
                "model": request.form.get('device_model'),
                "os_version": request.form.get('os_version'),
                "app_version": request.form.get('app_version')
            },
            "damage_type": request.form.get('damage_type'),
            "notes": request.form.get('notes')
        }
        
        # Save metadata
        metadata_file = save_metadata(photo_id, metadata)
        
        # Queue for AI processing (in a real implementation)
        # ai_processor.queue_photo(save_path, metadata_file)
        
        logger.info(f"Photo uploaded: {photo_id} for job {job_id}")
        
        return jsonify({
            "photo_id": photo_id,
            "job_id": job_id,
            "status": "uploaded",
            "message": "Photo uploaded successfully and queued for processing"
        })
    
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/api/photos/<job_id>', methods=['GET'])
def get_job_photos(job_id):
    """Get all photos for a specific job."""
    # In a real implementation, this would validate the token
    # and check if the contractor has access to this job
    contractor_id = request.headers.get('X-Contractor-ID')
    
    if not contractor_id:
        return jsonify({"error": "Contractor ID required"}), 400
    
    # Check if job directory exists
    job_dir = os.path.join(UPLOAD_FOLDER, job_id)
    if not os.path.exists(job_dir):
        return jsonify({"error": "Job not found or no photos uploaded"}), 404
    
    # Get all photos for this job
    photos = []
    for filename in os.listdir(job_dir):
        if allowed_file(filename):
            photo_id = filename.split('.')[0]
            
            # Get metadata if available
            metadata_file = os.path.join(UPLOAD_FOLDER, 'metadata', f"{photo_id}.json")
            metadata = {}
            if os.path.exists(metadata_file):
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
            
            photos.append({
                "photo_id": photo_id,
                "filename": filename,
                "url": f"/api/photos/view/{job_id}/{filename}",
                "upload_time": metadata.get("upload_time", "Unknown"),
                "damage_type": metadata.get("damage_type", "Unknown"),
                "processing_status": metadata.get("processing_status", "pending")
            })
    
    return jsonify({
        "job_id": job_id,
        "contractor_id": contractor_id,
        "photo_count": len(photos),
        "photos": photos
    })

@app.route('/api/photos/view/<job_id>/<filename>', methods=['GET'])
def view_photo(job_id, filename):
    """View a specific photo."""
    return send_from_directory(os.path.join(UPLOAD_FOLDER, job_id), filename)

def main():
    """Run the Flask application."""
    parser = argparse.ArgumentParser(description="Photo Collection API")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the API on")
    parser.add_argument("--port", type=int, default=5000, help="Port to run the API on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    args = parser.parse_args()
    
    logger.info(f"Starting Photo Collection API on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()
