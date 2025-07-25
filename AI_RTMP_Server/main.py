import asyncio
import base64
import cv2
import numpy as np
import torch
import os
import shutil
import re
from ultralytics import YOLO
from gradio_client import Client, handle_file  # Replaced deepface
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form, HTTPException, status
import time

# --- 1. Configuration and Client Loading ---

app = FastAPI(
    title="Drishti AI Processing Service",
    description="A real-time AI service using a Gradio backend for face recognition.",
    version="3.0.0"
)

# Use 'cuda' if GPU is available, otherwise 'cpu'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"INFO: Using device: {DEVICE}")

try:
    # Load local YOLOv8 model for person detection
    yolo_model = YOLO("yolov8n.pt").to(DEVICE)
    print("INFO: YOLOv8 model loaded successfully.")

    # Instantiate the Gradio client to connect to your Hugging Face Space
    gradio_client = Client("pushpenderindia/deepface")
    print("INFO: Gradio client connected to Hugging Face Space.")
except Exception as e:
    print(f"ERROR: Failed to load models or clients: {e}")
    exit()

# Configuration for the local directory of known faces
KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)


# --- 2. Helper Functions (Unchanged) ---

def get_crowd_risk(density):
    if density < 0.0001: return 'Low'
    elif density < 0.00015: return 'Medium'
    elif density < 0.0002: return 'High'
    else: return 'Critical'

def get_crowd_status(density):
    if density < 0.0001: return 'Stable'
    elif density < 0.00015: return 'Unstable'
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
    resized_frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
    enhanced_frame = enhance_frame(resized_frame)
    frame_area = resized_frame.shape[0] * resized_frame.shape[1]
    
    # A. Crowd Analysis with YOLOv8
    with torch.inference_mode():
        results = yolo_model(enhanced_frame, classes=[0], verbose=False)[0]
    annotated_frame = results.plot()
    people_count = len(results.boxes)
    density = people_count / frame_area if frame_area > 0 else 0
    risk = get_crowd_risk(density)
    status = get_crowd_status(density)
    
    # B. Face Recognition using Gradio Client (Replaces DeepFace)
    detected_persons = []
    known_face_files = [f for f in os.listdir(KNOWN_FACES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Periodically run the expensive face recognition process
    if known_face_files and people_count > 0 and frame_count % 90 == 0: # Reduced frequency due to API calls
        detected_person_boxes = [box.xyxy[0].cpu().numpy().astype(int) for box in results.boxes]

        for box in detected_person_boxes:
            x1, y1, x2, y2 = box
            detected_face_img = resized_frame[y1:y2, x1:x2]

            # Skip if the cropped image is too small
            if detected_face_img.shape[0] < 30 or detected_face_img.shape[1] < 30:
                continue

            temp_face_path = f"temp_face_{int(time.time()*1000)}.jpg"
            cv2.imwrite(temp_face_path, detected_face_img)

            try:
                for known_filename in known_face_files:
                    known_face_path = os.path.join(KNOWN_FACES_DIR, known_filename)
                    
                    # Call the Hugging Face API
                    result_str = gradio_client.predict(
                        img1=handle_file(temp_face_path),
                        img2=handle_file(known_face_path),
                        api_name="/predict"
                    )
                    
                    if "Match Found" in result_str:
                        person_name = os.path.splitext(known_filename)[0].replace("_", " ").title()
                        detected_persons.append(person_name)
                        break # Found a match, no need to check against other known faces for this person
            finally:
                if os.path.exists(temp_face_path):
                    os.remove(temp_face_path) # Clean up temporary file

    # C. Annotate Frame with Metrics
    y0 = 20
    info_text = [
        f"People Count: {people_count}", f"Density: {density:.6f}",
        f"Risk Level: {risk}", f"Crowd Status: {status}",
    ]
    if detected_persons:
        info_text.append(f"Detected: {', '.join(sorted(list(set(detected_persons))))}")
    for line in info_text:
        (tw, th), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(annotated_frame, (5, y0 - th - 5), (10 + tw, y0 + 5), (0, 0, 0), -1)
        cv2.putText(annotated_frame, line, (10, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y0 += th + 15

    # D. Prepare JSON Payload
    metrics_json = {
        "people_count": people_count, "density": round(density, 6),
        "risk": risk, "status": status,
        "detected_persons": sorted(list(set(detected_persons)))
    }
    return annotated_frame, metrics_json

# --- 4. WebSocket Endpoint for Live Streaming ---
@app.websocket("/ws/{stream_key}")
async def websocket_endpoint(websocket: WebSocket, stream_key: str):
    await websocket.accept()
    rtmp_url = f"rtmp://nginx-rtmp:1935/live/{stream_key}"
    cap = cv2.VideoCapture(rtmp_url)
    if not cap.isOpened():
        await websocket.close(code=1011)
        return
    frame_count = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                await asyncio.sleep(0.1)
                continue
            annotated_frame, metrics = process_frame_realtime(frame, frame_count)
            frame_count += 1
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            await websocket.send_json({"image": jpg_as_text, "metrics": metrics})
            await asyncio.sleep(0.01)
    except WebSocketDisconnect:
        print(f"INFO: Client disconnected from stream: {stream_key}")
    finally:
        cap.release()

# --- 5. API Endpoints for Face Management (Updated) ---
@app.get("/faces", tags=["Face Management"])
async def get_known_faces():
    """Retrieves a list of all known faces from the database directory."""
    try:
        faces = [os.path.splitext(f)[0] for f in os.listdir(KNOWN_FACES_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        return {"known_faces": faces}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/faces", status_code=status.HTTP_201_CREATED, tags=["Face Management"])
async def add_known_face(name: str = Form(...), file: UploadFile = File(...)):
    """Adds a new face to the database."""
    safe_name = re.sub(r'[^a-z0-9_]', '', name.lower().replace(' ', '_'))
    if not safe_name:
        raise HTTPException(status_code=400, detail="Invalid name.")
    file_extension = os.path.splitext(file.filename)[1]
    if file_extension.lower() not in ['.png', '.jpg', '.jpeg']:
        raise HTTPException(status_code=400, detail="Invalid file type.")
    file_path = os.path.join(KNOWN_FACES_DIR, f"{safe_name}{file_extension}")
    if os.path.exists(file_path):
        raise HTTPException(status_code=409, detail=f"A face with the name '{safe_name}' already exists.")
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    return {"message": "Face added successfully", "name": safe_name, "file_path": file_path}

@app.delete("/faces/{face_name}", status_code=status.HTTP_200_OK, tags=["Face Management"])
async def delete_known_face(face_name: str):
    """Deletes a face from the database by its name."""
    file_to_delete = None
    for f in os.listdir(KNOWN_FACES_DIR):
        if os.path.splitext(f)[0] == face_name:
            file_to_delete = os.path.join(KNOWN_FACES_DIR, f)
            break
    if not file_to_delete:
        raise HTTPException(status_code=404, detail=f"Face '{face_name}' not found.")
    try:
        os.remove(file_to_delete)
        return {"message": f"Face '{face_name}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {e}")