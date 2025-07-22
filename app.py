from flask import Flask, render_template, request, jsonify, url_for
import os
from dotenv import load_dotenv
from gradio_client import Client, handle_file
import json
import requests
from werkzeug.utils import secure_filename
import uuid
import tempfile
import time

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

@app.route('/live_feed')
def live_feed():
    return render_template('live_feed.html',
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
        import traceback
        traceback.print_exc()
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
        
        # Initialize Gradio client
        client = Client(AI_SERVER_URL)
        
        # Use handle_file for local file processing
        result = client.predict(
            {"video": handle_file(video_url)},  # Use handle_file for local files
            skip,
            max_workers,
            api_name="/predict"
        )
        
        # Log the result structure for debugging
        print(f"Prediction result received: {result}")
        
        # Check if the response includes a video path
        if isinstance(result, tuple) and len(result) >= 3:
            video_dict = result[0]
            plot_dict = result[1]
            realtime_metrics_list = result[2] 
            
            # Convert relative paths to absolute URLs if needed
            if isinstance(video_dict, dict) and 'video' in video_dict:
                video_path = video_dict['video']
                if video_path.startswith('/'):
                    # This is a local path - serve it as a static file
                    video_url_path = f"/static/processed/{os.path.basename(video_path)}"
                    os.makedirs(os.path.dirname(os.path.join('static', 'processed')), exist_ok=True)
                    
                    # Copy the file to our static directory if it exists
                    if os.path.exists(video_path):
                        target_path = os.path.join('static', 'processed', os.path.basename(video_path))
                        import shutil
                        shutil.copy(video_path, target_path)
                        video_dict['video'] = video_url_path
            
            # Process metrics data if needed
            if realtime_metrics_list:
                print(f"Received metrics data with {len(realtime_metrics_list)} data points")
                
                # Generate summary statistics
                if len(realtime_metrics_list) > 0:
                    avg_people = sum(item['average_people'] for item in realtime_metrics_list) / len(realtime_metrics_list)
                    max_people = max(item['average_people'] for item in realtime_metrics_list)
                    
                    print(f"Average people count: {avg_people}")
                    print(f"Maximum people count: {max_people}")
        
        # Return the raw prediction results
        return jsonify({
            'status': 'success',
            'data': result
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