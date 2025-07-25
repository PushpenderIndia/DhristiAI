from flask import Flask, render_template, request, jsonify, url_for, flash, redirect, send_from_directory
import os
from dotenv import load_dotenv
from gradio_client import Client, handle_file
import json
import requests
from werkzeug.utils import secure_filename
import uuid
import tempfile
import time
from flask_pymongo import PyMongo 
from bson.objectid import ObjectId
import telegram
from telegram import Bot

# Load environment variables
load_dotenv()

app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.secret_key = os.urandom(24) 
mongo = PyMongo(app)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max upload size
# Ensure the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Get environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
AI_SERVER_URL = os.getenv('AI_SERVER_URL')
RTMP_SERVER_URL = os.getenv('RTMP_SERVER_URL')
FACE_RECOGNITION_AI_SERVER_URL = os.getenv('FACE_RECOGNITION_AI_SERVER_URL')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_BOT = Bot(token=TELEGRAM_BOT_TOKEN) if TELEGRAM_BOT_TOKEN else None

def send_telegram_notification(receiver, message, image_path=None):
    if not TELEGRAM_BOT:
        print('Telegram bot not configured.')
        return
    try:
        # If receiver is username, ensure it starts with @
        if receiver and not receiver.startswith('@') and not receiver.startswith('+'):
            receiver = '@' + receiver
        if image_path:
            with open(image_path, 'rb') as img:
                TELEGRAM_BOT.send_photo(chat_id=receiver, photo=img, caption=message)
        else:
            TELEGRAM_BOT.send_message(chat_id=receiver, text=message)
    except Exception as e:
        print(f'Failed to send Telegram message: {e}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    try:
        cameras = list(mongo.db.cameras.find())
    except Exception as e:
        cameras = []

    print(f"Loaded {len(cameras)} cameras from the database")
    return render_template('dashboard.html', 
                          ai_server_url=AI_SERVER_URL,
                          cameras=len(cameras)) 

@app.route('/live_feed')
def live_feed():
    try:
        cameras = list(mongo.db.cameras.find())
    except Exception as e:
        cameras = []
    return render_template('live_feed.html',
                          ai_server_url=AI_SERVER_URL,
                          cameras=cameras)

@app.route('/live_feed_rtmp')
def live_feed_rtmp():
    try:
        cameras = list(mongo.db.cameras.find())
    except Exception as e:
        cameras = []
    return render_template('live_feed_rtmp.html',
                          ai_server_url=AI_SERVER_URL,
                          cameras=cameras)

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

@app.route('/add_camera', methods=['POST'])
def add_camera():
    camera_url = request.form.get('camera_url').strip()

    if not camera_url:
        flash('Camera URL cannot be empty.', 'error')
        return redirect(url_for('live_feed'))

    # Ensure URL has http:// prefix
    if not camera_url.startswith('http://') and not camera_url.startswith('https://'):
        camera_url = 'http://' + camera_url
    
    # Remove trailing slash
    if camera_url.endswith('/'):
        camera_url = camera_url[:-1]

    # Check if camera already exists
    try:
        already_exists = mongo.db.cameras.find_one({'url': camera_url})
    except Exception as e:
        already_exists = None
    if already_exists:
        flash('This camera has already been added.', 'warning')
    else:
        mongo.db.cameras.insert_one({
            'url': camera_url,
            'dateAdded': time.time()
        })
        flash('Camera added successfully!', 'success')

    return redirect(url_for('live_feed'))

@app.route('/add_camera_rtmp', methods=['POST'])
def add_camera_rtmp():
    camera_name = request.form.get('camera_name', '').strip()
    stream_key = request.form.get('stream_key', '').strip()

    if not camera_name or not stream_key:
        flash('Camera Name and Stream Key cannot be empty.', 'error')
        return redirect(url_for('live_feed'))

    # Check if stream key already exists
    if mongo.db.cameras.find_one({'stream_key': stream_key}):
        flash('This Stream Key is already in use.', 'warning')
    else:
        # Generate the URLs based on your NGINX server setup
        # NOTE: Use your server's public IP or domain name, not localhost.
        server_ip = RTMP_SERVER_URL #"34.100.129.109" 

        rtmp_push_url = f"rtmp://{server_ip}:1935/live/{stream_key}"
        hls_playback_url = f"http://{server_ip}:8080/hls/{stream_key}.m3u8"

        mongo.db.cameras.insert_one({
            'name': camera_name,
            'stream_key': stream_key,
            'rtmp_push_url': rtmp_push_url,
            'hls_playback_url': hls_playback_url,
            'dateAdded': time.time()
        })
        flash('Camera stream added successfully!', 'success')

    return redirect(url_for('live_feed_rtmp'))

@app.route('/delete_camera/<camera_id>', methods=['POST'])
def delete_camera(camera_id):
    try:
        # The camera_id from the URL is a string, it needs to be converted to an ObjectId
        result = mongo.db.cameras.delete_one({'_id': ObjectId(camera_id)})
        if result.deleted_count > 0:
            flash('Camera removed successfully.', 'success')
        else:
            flash('Camera not found.', 'error')
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        
    return redirect(url_for('live_feed'))

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

@app.route('/find_person', methods=['GET', 'POST'])
def find_person():
    if request.method == 'GET':
        return render_template('missing_person.html')
    try:
        person_name = request.form.get('person_name', '').strip()
        person_image = request.files.get('person_image')
        telegram_receiver = request.form.get('telegram_receiver', '').strip()
        if not person_name or not person_image or not telegram_receiver:
            return jsonify({'status': 'error', 'message': 'Name, image, and Telegram receiver are required.'}), 400
        filename = secure_filename(f"{uuid.uuid4()}_{person_image.filename}")
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        person_image.save(temp_path)
        cameras = list(mongo.db.cameras.find())
        results = []
        found = False
        found_result = None
        for cam in cameras:
            cam_url = cam.get('url')
            cam_name = cam.get('name', '')
            if not cam_url:
                continue
            frame_url = cam_url.rstrip('/') + '/photo.jpg'
            try:
                resp = requests.get(frame_url, timeout=3)
                if resp.status_code == 200:
                    frame_filename = f"{uuid.uuid4()}_frame.jpg"
                    frame_path = os.path.join(app.config['UPLOAD_FOLDER'], frame_filename)
                    with open(frame_path, 'wb') as f:
                        f.write(resp.content)
                    client = Client(FACE_RECOGNITION_AI_SERVER_URL)
                    result = client.predict(
                        img1=handle_file(frame_path),
                        img2=handle_file(temp_path),
                        api_name="/predict"
                    )
                    result_str = str(result)
                    is_match = result_str.strip().lower().startswith('match found')
                    similarity = None
                    import re
                    match = re.search(r'Similarity(?: Score)?: ([0-9.]+)', result_str)
                    if match:
                        similarity = match.group(1)
                    frame_url_out = None
                    if is_match:
                        processed_dir = os.path.join('static', 'processed')
                        os.makedirs(processed_dir, exist_ok=True)
                        processed_filename = f"{uuid.uuid4()}_frame.jpg"
                        processed_path = os.path.join(processed_dir, processed_filename)
                        import shutil
                        shutil.copy(frame_path, processed_path)
                        frame_url_out = url_for('static', filename=f'processed/{processed_filename}')
                        # Send Telegram notification for match
                        msg = f"✅ Person '{person_name}' FOUND!\nCamera: {cam_name or cam_url}\nSimilarity Score: {similarity if similarity else '?'}"
                        send_telegram_notification(telegram_receiver, msg, processed_path)
                        found = True
                        found_result = {'camera': cam_url, 'camera_name': cam_name, 'result': result_str, 'is_match': is_match, 'similarity': similarity, 'frame_url': frame_url_out}
                    results.append({
                        'camera': cam_url,
                        'camera_name': cam_name,
                        'result': result_str,
                        'is_match': is_match,
                        'similarity': similarity,
                        'frame_url': frame_url_out
                    })
                    os.remove(frame_path)
                else:
                    results.append({'camera': cam_url, 'camera_name': cam_name, 'result': 'Camera offline or no image.', 'is_match': False, 'similarity': None, 'frame_url': None})
            except Exception as e:
                results.append({'camera': cam_url, 'camera_name': cam_name, 'result': f'Error: {e}', 'is_match': False, 'similarity': None, 'frame_url': None})
        os.remove(temp_path)
        # If no match found, send not found message
        if not found:
            msg = f"❌ Sorry, person '{person_name}' was NOT found on any camera. We will keep monitoring."
            send_telegram_notification(telegram_receiver, msg)
        return jsonify({'status': 'success', 'results': results})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 