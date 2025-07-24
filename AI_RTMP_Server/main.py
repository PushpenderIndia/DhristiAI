import asyncio
import base64
import cv2
import numpy as np
import torch
import os
import shutil
import re
from ultralytics import YOLO
from deepface import DeepFace
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form, HTTPException, status

# --- 1. Configuration and Model Loading ---

app = FastAPI(
    title="Drishti AI Processing Service",
    description="A real-time AI service for crowd and face analysis via WebSockets and REST API.",
    version="1.1.0"
)

# Use 'cuda' if GPU is available, otherwise 'cpu'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"INFO: Using device: {DEVICE}")

# Load and optimize YOLOv8 model once
try:
    model = YOLO("yolov8n.pt").to(DEVICE)
    print("INFO: YOLOv8 model loaded successfully.")
except Exception as e:
    print(f"ERROR: Failed to load YOLO model: {e}")
    exit()

# Configuration for DeepFace
DEEPFACE_DB_PATH = "known_faces"
# Ensure the database directory exists
os.makedirs(DEEPFACE_DB_PATH, exist_ok=True)


# --- 2. Helper Functions ---

def get_crowd_risk(density):
    if density < 0.0001: return 'Low'
    elif density < 0.00015: return 'Medium'
    elif density < 0.0002: return 'High'
    else: return 'Critical'

def get_crowd_status(density):
    if density < 0.0001: return 'Stable'
    elif density < 0.00015: return 'Unstable'
    elif density < 0.0002: return 'Congested'
    else: return 'Critical'

def enhance_frame(frame, clipLimit=2.0, tileGrid=(8,8)):
    """Enhances frame contrast using CLAHE."""
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGrid)
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


# --- 3. Real-time Frame Processing Logic ---

def process_frame_realtime(frame, frame_count):
    """
    Processes a single frame for crowd counting and face recognition.
    """
    # Resize frame for consistent processing
    resized_frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
    enhanced_frame = enhance_frame(resized_frame)
    frame_area = resized_frame.shape[0] * resized_frame.shape[1]
    
    # A. Crowd Analysis with YOLOv8
    with torch.inference_mode():
        results = model(enhanced_frame, classes=[0], verbose=False)[0]

    annotated_frame = results.plot()
    people_count = 0
    for box in results.boxes:
        if results.names[int(box.cls[0])] == 'person':
            people_count += 1

    density = people_count / frame_area if frame_area > 0 else 0
    risk = get_crowd_risk(density)
    status = get_crowd_status(density)
    
    # B. Face Recognition with DeepFace
    detected_persons = []
    # Check if DB is not empty and run recognition periodically
    if os.listdir(DEEPFACE_DB_PATH) and frame_count % 30 == 0 and people_count > 0:
        try:
            dfs = DeepFace.find(
                img_path=resized_frame,
                db_path=DEEPFACE_DB_PATH,
                enforce_detection=False,
                silent=True,
                detector_backend='retinaface'
            )
            unique_identities = set()
            for df in dfs:
                if not df.empty:
                    for identity_path in df['identity']:
                        name = os.path.splitext(os.path.basename(identity_path))[0].replace("_", " ").title()
                        unique_identities.add(name)
            detected_persons = list(unique_identities)
        except Exception as e:
            print(f"WARNING: DeepFace recognition error: {e}")

    # C. Annotate Frame with Metrics... (rest of the function is the same)
    y0 = 20
    info_text = [
        f"People Count: {people_count}",
        f"Density: {density:.6f}",
        f"Risk Level: {risk}",
        f"Crowd Status: {status}",
    ]
    if detected_persons:
        info_text.append(f"Detected: {', '.join(detected_persons)}")

    for line in info_text:
        (tw, th), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(annotated_frame, (5, y0 - th - 5), (10 + tw, y0 + 5), (0, 0, 0), -1)
        cv2.putText(annotated_frame, line, (10, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y0 += th + 15

    # D. Prepare JSON Payload
    metrics_json = {
        "people_count": people_count,
        "density": round(density, 6),
        "risk": risk,
        "status": status,
        "detected_persons": detected_persons
    }
    return annotated_frame, metrics_json


# --- 4. WebSocket Endpoint for Live Streaming ---

@app.websocket("/ws/{stream_key}")
async def websocket_endpoint(websocket: WebSocket, stream_key: str):
    # This function remains unchanged...
    await websocket.accept()
    print(f"INFO: WebSocket connection accepted for stream key: {stream_key}")
    rtmp_url = f"rtmp://localhost:1935/live/{stream_key}"
    cap = cv2.VideoCapture(rtmp_url)
    if not cap.isOpened():
        print(f"ERROR: Failed to open RTSP stream: {rtmp_url}")
        await websocket.close(code=1011, reason=f"Cannot connect to stream: {stream_key}")
        return
    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            annotated_frame, metrics = process_frame_realtime(frame, frame_count)
            frame_count += 1
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send_json({"image": jpg_as_text, "metrics": metrics})
            await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        print(f"INFO: Client disconnected from stream: {stream_key}")
    except Exception as e:
        print(f"ERROR: An error occurred in the WebSocket for {stream_key}: {e}")
    finally:
        cap.release()
        print(f"INFO: Stream released and connection closed for {stream_key}")


# --- 5. NEW: API Endpoints for Face Management ---

@app.get("/faces", tags=["Face Management"])
async def get_known_faces():
    """
    Retrieves a list of all known faces from the database directory.
    """
    try:
        faces = [os.path.splitext(f)[0] for f in os.listdir(DEEPFACE_DB_PATH) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        return {"known_faces": faces}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/faces", status_code=status.HTTP_201_CREATED, tags=["Face Management"])
async def add_known_face(name: str = Form(...), file: UploadFile = File(...)):
    """
    Adds a new face to the database. The name is provided in a form field,
    and the image is uploaded as a file.
    """
    # Sanitize the name to create a safe filename
    safe_name = re.sub(r'[^a-z0-9_]', '', name.lower().replace(' ', '_'))
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid name. Name must contain alphanumeric characters.")

    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in ['.png', '.jpg', '.jpeg']:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .png, .jpg, or .jpeg image.")

    file_path = os.path.join(DEEPFACE_DB_PATH, f"{safe_name}{file_extension}")

    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail=f"A face with the name '{safe_name}' already exists.")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Clear DeepFace's cached representations to ensure the new face is found
        if os.path.exists(os.path.join(DEEPFACE_DB_PATH, "representations_vgg_face.pkl")):
            os.remove(os.path.join(DEEPFACE_DB_PATH, "representations_vgg_face.pkl"))
            print("INFO: DeepFace cache cleared.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")

    return {"message": "Face added successfully", "name": safe_name, "file_path": file_path}

@app.delete("/faces/{face_name}", status_code=status.HTTP_200_OK, tags=["Face Management"])
async def delete_known_face(face_name: str):
    """
    Deletes a face from the database by its name.
    """
    file_to_delete = None
    for f in os.listdir(DEEPFACE_DB_PATH):
        if os.path.splitext(f)[0] == face_name:
            file_to_delete = os.path.join(DEEPFACE_DB_PATH, f)
            break

    if not file_to_delete:
        raise HTTPException(status_code=404, detail=f"Face '{face_name}' not found.")

    try:
        os.remove(file_to_delete)
        # Clear DeepFace cache after deletion as well
        if os.path.exists(os.path.join(DEEPFACE_DB_PATH, "representations_vgg_face.pkl")):
            os.remove(os.path.join(DEEPFACE_DB_PATH, "representations_vgg_face.pkl"))
            print("INFO: DeepFace cache cleared after deletion.")

        return {"message": f"Face '{face_name}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {e}")