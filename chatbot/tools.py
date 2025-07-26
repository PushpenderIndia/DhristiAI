import os, uuid, shutil, re, requests
from gradio_client import Client, handle_file
from flask_pymongo import PyMongo
from flask import current_app

def run_find_person(name: str, image_path_local: str) -> dict:
    """
    Search for a person across cameras.
    """
    mongo = PyMongo(current_app)
    cameras = list(mongo.db.cameras.find())
    results = []
    found = False

    for cam in cameras:
        cam_url = cam.get('url')
        cam_name = cam.get('name') or cam_url
        frame_url = cam_url.rstrip('/') + '/photo.jpg'
        try:
            resp = requests.get(frame_url, timeout=5)
            if resp.status_code == 200:
                frame_fp = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_frame.jpg")
                with open(frame_fp, 'wb') as f:
                    f.write(resp.content)
                client = Client(current_app.config['FACE_RECOGNITION_AI_SERVER_URL'])
                result = client.predict(
                    img1=handle_file(frame_fp), img2=handle_file(image_path_local), api_name="/predict"
                )
                result_str = str(result)
                is_match = result_str.lower().strip().startswith('match found')
                similarity = None
                m = re.search(r'Similarity(?: Score)?: ([0-9.]+)', result_str)
                if m: similarity = m.group(1)
                frame_url_out = None
                if is_match:
                    proc = os.path.join('static','processed')
                    os.makedirs(proc, exist_ok=True)
                    pname = f"{uuid.uuid4()}_frame.jpg"
                    shutil.copy(frame_fp, os.path.join(proc, pname))
                    frame_url_out = f"/static/processed/{pname}"
                    found = True
                results.append({
                    'camera': cam_url, 'camera_name': cam_name,
                    'result': result_str, 'is_match': is_match,
                    'similarity': similarity, 'frame_url': frame_url_out
                })
            else:
                results.append({'camera': cam_url, 'camera_name': cam_name,
                                'result': 'No image retrieved', 'is_match': False,
                                'similarity': None, 'frame_url': None})
        except Exception as e:
            results.append({'camera': cam_url, 'camera_name': cam_name,
                            'result': f'Error: {e}', 'is_match': False,
                            'similarity': None, 'frame_url': None})
    return {'status': 'success', 'found': found, 'results': results}
