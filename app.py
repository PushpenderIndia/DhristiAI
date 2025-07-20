from flask import Flask, render_template, request, jsonify, url_for
import os
from dotenv import load_dotenv
from gradio_client import Client
import json
import requests
from werkzeug.utils import secure_filename
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload size
# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Get environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
AI_SERVER_URL = os.getenv('AI_SERVER_URL')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', 
                          ai_server_url=AI_SERVER_URL)

@app.route('/api/upload_video', methods=['POST'])
def upload_video():
    try:
        # Check if a video file was uploaded
        if 'video' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No video file provided'
            }), 400
        
        video = request.files['video']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if video.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No video file selected'
            }), 400
        
        # Generate unique filename to avoid conflicts
        filename = secure_filename(f"{uuid.uuid4()}_{video.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save the uploaded file
        video.save(file_path)
        
        # Return the file path to be used by predict API
        return jsonify({
            'status': 'success',
            'video_url': file_path,
            'message': 'Video uploaded successfully'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        video_url = data.get('video_url')
        skip = int(data.get('skip', 2))
        max_workers = int(data.get('max_workers', 1))
        
        if not video_url:
            return jsonify({
                'status': 'error',
                'message': 'Video URL is required'
            }), 400
        
        print(f"Processing video: {video_url} with skip={skip}, max_workers={max_workers}")
        
        # Initialize Gradio client with the AI server URL
        client = Client(AI_SERVER_URL)
        
        # Make prediction with positional arguments instead of keyword arguments
        # The Gradio API expects inputs as positional arguments
        result = client.predict(
            {"video": video_url},  # First parameter is the video
            skip,                  # Second parameter is skip
            max_workers,           # Third parameter is max_workers
            api_name="/predict"
        )
        
        print(f"Prediction result received: {result}")
        
        # Return the raw prediction results to let frontend handle formatting
        return jsonify({
            'status': 'success',
            'data': result  # Raw result from Gradio API
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 