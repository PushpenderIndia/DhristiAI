import cv2
import numpy as np
from ultralytics import YOLO
import imutils
import subprocess
import time
from collections import deque
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Load YOLOv8 model (trained to detect humans)
model = YOLO('yolov8s.pt')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_CHANNEL_ID = int(os.getenv('TELEGRAM_CHANNEL_ID'))

def send_telegram_message(receiver, message):
    if not TELEGRAM_BOT_TOKEN:
        print('Telegram bot not configured.')
        return
    # Only check .startswith if receiver is a string
    if isinstance(receiver, str) and not receiver.startswith('@') and not receiver.startswith('+'):
        receiver = '@' + receiver
    url = f"{TELEGRAM_API_URL}/sendMessage"
    data = {
        "chat_id": receiver,
        "text": message
    }
    try:
        resp = requests.post(url, data=data)
        print("Telegram message sent:", resp.text)
    except Exception as e:
        print("Telegram send error:", e)

def count_people_live_camera(showCam, input_video, rtmp_url, line_position=300, direction='down', threshold_count=30):
    """Version for live camera input with proper frame rate control"""
    send_counter = 0
    if showCam:
        cap = cv2.VideoCapture(0)
        # For live camera, use 30 FPS
        fps = 30
    else:
        cap = cv2.VideoCapture(input_video)
        # Get the original video's FPS
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:  # Fallback if FPS detection fails
            fps = 30
    
    print(f"Using FPS: {fps}")
    
    # Set camera properties (only applies to live camera)
    if showCam:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, fps)
    
    width = 800
    height = 600
    
    # Calculate frame interval for timing control
    frame_interval = 1.0 / fps
    
    # FFmpeg command for RTMP streaming
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', f'{width}x{height}',
        '-r', str(fps),  # Use the actual video FPS
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        '-tune', 'zerolatency',
        '-g', str(int(fps * 2)),  # Keyframe interval
        '-b:v', '2500k',
        '-maxrate', '2500k',
        '-bufsize', '5000k',
        '-f', 'flv',
        rtmp_url
    ]
    
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    tracked = {}
    next_id = 0
    total_count = 0
    
    # For frame timing
    last_frame_time = time.time()
    frame_count = 0

    try:
        while True:
            start_time = time.time()
            
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame or end of video")
                break

            frame = imutils.resize(frame, width=width)
            results = model(frame)[0]
            centroids = []

            for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
                if int(cls) != 0:
                    continue
                x1, y1, x2, y2 = map(int, box)
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                centroids.append((cx, cy))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Tracking and counting logic
            new_tracked = {}
            for c in centroids:
                assigned = False
                for id, (old_c, counted) in tracked.items():
                    if np.linalg.norm(np.array(c) - np.array(old_c)) < 50:
                        new_tracked[id] = (c, counted)
                        assigned = True
                        break
                if not assigned:
                    new_tracked[next_id] = (c, False)
                    next_id += 1

            for id, (c, counted) in new_tracked.items():
                if not counted:
                    if direction == 'down' and c[1] > line_position:
                        total_count += 1
                        new_tracked[id] = (c, True)
                    elif direction == 'up' and c[1] < line_position:
                        total_count += 1
                        new_tracked[id] = (c, True)

            tracked = new_tracked

            # Draw counting line and status
            cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (0, 0, 255), 2)
            
            # Add status text with better formatting
            if total_count > threshold_count:
                # Alert status
                status_text = f'CAPACITY REACHED: {total_count}/{threshold_count}'
                text_color = (0, 0, 255)  # Red
                bg_color = (0, 0, 0)  # Black background
                
                # Calculate text size and position
                font_scale = 0.8
                thickness = 2
                text_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
                
                # Draw background rectangle
                cv2.rectangle(frame, (5, 5), (text_size[0] + 15, text_size[1] + 15), bg_color, -1)
                cv2.putText(frame, status_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)
                if send_counter < 1:
                    send_telegram_message(TELEGRAM_CHANNEL_ID, "⚠️" + status_text + "\n\nClose the venue gate immediately")
                    send_counter += 1
            else:
                # Normal status
                status_text = f'Count: {total_count}/{threshold_count}'
                text_color = (0, 255, 0)  # Green
                bg_color = (0, 0, 0)  # Black background
                
                # Calculate text size and position
                font_scale = 0.8
                thickness = 2
                text_size = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
                
                # Draw background rectangle
                cv2.rectangle(frame, (5, 5), (text_size[0] + 15, text_size[1] + 15), bg_color, -1)
                cv2.putText(frame, status_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)
            
            # Add FPS counter for debugging
            current_time = time.time()
            if current_time - last_frame_time >= 1.0:
                actual_fps = frame_count / (current_time - last_frame_time)
                last_frame_time = current_time
                frame_count = 0
                print(f"Processing FPS: {actual_fps:.1f}, Target FPS: {fps}")
            frame_count += 1
            
            # Write to RTMP stream
            try:
                ffmpeg_process.stdin.write(frame.tobytes())
                ffmpeg_process.stdin.flush()  # Ensure data is sent immediately
            except BrokenPipeError:
                print("FFmpeg process terminated")
                break
            
            # Optional local display
            cv2.imshow('AI Gate Entrance Guard', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Frame rate control - this is the key fix!
            processing_time = time.time() - start_time
            sleep_time = frame_interval - processing_time
            
            if sleep_time > 0:
                time.sleep(sleep_time)
            elif not showCam:  # Only warn for video files, not live camera
                print(f"Warning: Processing too slow! Target: {frame_interval:.3f}s, Actual: {processing_time:.3f}s")

    except KeyboardInterrupt:
        print("Live streaming interrupted")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if ffmpeg_process.poll() is None:
            ffmpeg_process.stdin.close()
            ffmpeg_process.terminate()
            ffmpeg_process.wait()
        
        print(f"Final count: {total_count}")

if __name__ == '__main__':
    # Configuration
    showCam = False  # Set to True for live camera, False for video file
    rtmp_url = 'rtmp://test.antmedia.io/WebRTCAppEE/streamId_zA44avZub'
    video_path = 'DemoVideos/Crowd_Low_Density.mp4'
    
    count_people_live_camera(showCam, video_path, rtmp_url)