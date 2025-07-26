import cv2
import numpy as np
from ultralytics import YOLO
import imutils
from collections import deque

# Load YOLOv8 model (trained to detect humans)
model = YOLO('yolov8s.pt')

def count_people(input_video, line_position=300, direction='down', threshold_count=30):
    cap = cv2.VideoCapture(input_video)
    tracked = {}  # track human centroids by ID
    next_id = 0
    total_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=800)
        results = model(frame)[0]
        centroids = []

        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            if int(cls) != 0:
                continue  # skip non-person classes
            x1, y1, x2, y2 = map(int, box)
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            centroids.append((cx, cy))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Simple tracking by association
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

        # Counting logic: if centroid crosses line
        for id, (c, counted) in new_tracked.items():
            if not counted:
                if direction == 'down' and c[1] > line_position:
                    total_count += 1
                    new_tracked[id] = (c, True)
                elif direction == 'up' and c[1] < line_position:
                    total_count += 1
                    new_tracked[id] = (c, True)

        tracked = new_tracked

        cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (0, 0, 255), 2)
        if total_count > threshold_count:
            # Alert message with background
            font_scale = 0.7
            font_thickness = 2
            alert_text = f'VENUE AT CAPACITY - STOP ADMISSION'
            count_text = f'Current: {total_count} | Limit: {threshold_count}'
            
            # Calculate text sizes
            alert_size, _ = cv2.getTextSize(alert_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            count_size, _ = cv2.getTextSize(count_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale * 0.8, font_thickness)
            
            # Position text in center
            alert_x = (frame.shape[1] - alert_size[0]) // 2
            alert_y = (frame.shape[0] + alert_size[1]) // 2 - 20
            count_x = (frame.shape[1] - count_size[0]) // 2
            count_y = alert_y + alert_size[1] + 10
            
            # Draw background rectangles
            padding = 10
            alert_bg_rect = [
                (alert_x - padding, alert_y - alert_size[1] - padding),
                (alert_x + alert_size[0] + padding, alert_y + padding)
            ]
            count_bg_rect = [
                (count_x - padding, count_y - count_size[1] - padding),
                (count_x + count_size[0] + padding, count_y + padding)
            ]
            
            # Draw backgrounds
            cv2.rectangle(frame, alert_bg_rect[0], alert_bg_rect[1], (0, 0, 0), -1)  # Black background
            cv2.rectangle(frame, count_bg_rect[0], count_bg_rect[1], (0, 0, 0), -1)  # Black background
            
            # Draw text
            cv2.putText(frame, alert_text, (alert_x, alert_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), font_thickness)
            cv2.putText(frame, count_text, (count_x, count_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale * 0.8, (255, 255, 255), font_thickness)
        else:
            # Normal count display with background
            font_scale = 0.8
            font_thickness = 2
            status_text = f'VENUE STATUS: OPEN'
            count_text = f'Current Count: {total_count} / {threshold_count}'
            
            # Calculate text sizes
            status_size, _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            count_size, _ = cv2.getTextSize(count_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale * 0.9, font_thickness)
            
            # Position text
            status_x = 10
            status_y = 40
            count_x = 10
            count_y = status_y + status_size[1] + 10
            
            # Draw background rectangles
            padding = 8
            status_bg_rect = [
                (status_x - padding, status_y - status_size[1] - padding),
                (status_x + status_size[0] + padding, status_y + padding)
            ]
            count_bg_rect = [
                (count_x - padding, count_y - count_size[1] - padding),
                (count_x + count_size[0] + padding, count_y + padding)
            ]
            
            # Draw backgrounds
            cv2.rectangle(frame, status_bg_rect[0], status_bg_rect[1], (0, 0, 0), -1)  # Black background
            cv2.rectangle(frame, count_bg_rect[0], count_bg_rect[1], (0, 0, 0), -1)  # Black background
            
            # Draw text
            cv2.putText(frame, status_text, (status_x, status_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), font_thickness)
            cv2.putText(frame, count_text, (count_x, count_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale * 0.9, (255, 255, 255), font_thickness)
        cv2.imshow('People Counter', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print('Final count:', total_count)

if __name__ == '__main__':
    count_people('/Users/pushpendersingh/Documents/Hackathons/DhristiAI/DemoVideos/Crowd_Low_Density.mp4')
