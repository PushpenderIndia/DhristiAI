import gradio as gr
import cv2
import numpy as np
from ultralytics import YOLO
import tempfile
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import torch

# Determine dynamic worker count based on CPU cores
CPU_CORES = os.cpu_count() or 4
MAX_WORKERS = max(1, CPU_CORES - 1)

# # Load and optimize YOLOv8 model once on GPU
# model = YOLO("yolov8n.pt").to('cuda')
# model.fuse()  # fuse conv and batchnorm for speed
# model.eval()  # set to eval mode

# Load and optimize YOLOv8 model once on GPU
model = YOLO("yolov8n.pt").to('cpu')
model.fuse()  # fuse conv and batchnorm for speed
model.eval()  # set to eval mode

# Helper functions

def calculate_crowd_density(num_people, frame_area):
    return num_people / frame_area if frame_area > 0 else 0

def get_crowd_risk(density):
    if density < 0.00002:
        return 'Low'
    elif density < 0.00006:
        return 'Low'
    elif density < 0.0001:
        return 'Medium'
    elif density < 0.00015:
        return 'High'
    elif density < 0.0002:
        return 'High'
    else:
        return 'Critical'

def get_crowd_status(density):
    if density < 0.00002:
        return 'Free Flowing'
    elif density < 0.00006:
        return 'Stable'
    elif density < 0.0001:
        return 'Capacity'
    elif density < 0.00015:
        return 'Unstable'
    elif density < 0.0002:
        return 'Congested'
    else:
        return 'Critical'


def enhance_frame(frame, clipLimit=2.0, tileGrid=(8,8), gamma=1.5):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGrid)
    l = clahe.apply(l)
    lab = cv2.merge((l, a, b))
    frame_clahe = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(256)]).astype('uint8')
    return cv2.LUT(frame_clahe, table)


def process_frame(item, area):
    idx, frame = item
    frame_enh = enhance_frame(frame)
    with torch.inference_mode():  # disable gradients
        res = model(frame_enh, classes=[0], verbose=False)[0]
    annotated = res.plot()
    ppl = sum(1 for box in res.boxes if res.names[int(box.cls[0])] == 'person')
    dens = calculate_crowd_density(ppl, area)
    risk = get_crowd_risk(dens)
    status = get_crowd_status(dens)
    y0 = 10
    for line in [
        f'Real Time #People: {ppl}',
        f'Density: {dens:.6f}',
        f'Risk: {risk}',
        f'Status: {status}'
    ]:
        (tw, th), _ = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(annotated, (10, y0), (10 + tw + 4, y0 + th + 4), (0,0,0), -1)
        cv2.putText(annotated, line, (12, y0 + th + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        y0 += th + 10
    return idx, annotated, dens, ppl, risk, status

def process_video(video_path, skip=4, max_workers=MAX_WORKERS):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frames = []
    idx = 0
    width, height = 640, None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to width=640 while maintaining aspect ratio
        if height is None:
            h, w = frame.shape[:2]
            aspect_ratio = h / w
            height = int(width * aspect_ratio)

        resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
        frames.append((idx, resized_frame))
        idx += 1

    cap.release()

    area = width * height

    # Process frames in parallel
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_frame, f, area): f[0] for f in frames if f[0] % skip == 0}
        for future in as_completed(futures):
            results.append(future.result())

    # Build result lookup
    result_dict = {r[0]: (r[1], r[2], r[3], r[4], r[5]) for r in results}
    sorted_keys = sorted(result_dict.keys())

    # Prepare writer
    out_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

    densities = []
    people_counts = []
    risk_levels = []
    status_levels = []
    for i in range(len(frames)):
        if i in result_dict:
            annotated, dens, ppl, risk, status = result_dict[i]
        else:
            prev = [k for k in sorted_keys if k < i]
            closest = max(prev) if prev else sorted_keys[0]
            annotated, dens, ppl, risk, status = result_dict[closest]
        writer.write(annotated)
        densities.append(dens)
        people_counts.append(ppl)
        risk_levels.append(risk)
        status_levels.append(status)


    writer.release()

    # Plot density over time (unchanged)
    times = np.arange(len(densities)) / fps
    REG_THRESH = [0.00000, 0.00002, 0.00006, 0.00010, 0.00015, 0.00020]
    REG_LABELS = ["Free Flowing","Stable","Capacity","Unstable","Congested","Critical"]
    REG_COLORS = ["green","limegreen","gold","orange","orangered","red"]
    ymin, ymax = 0.0, max(max(densities)*1.1, REG_THRESH[-1] + 1e-6)
    stops = [t/ymax for t in REG_THRESH] + [1.0]
    cmap = LinearSegmentedColormap.from_list("risk_grad", list(zip(stops, REG_COLORS + [REG_COLORS[-1]])))

    fig, ax = plt.subplots(figsize=(12,6))
    gradient = np.linspace(ymin, ymax, 512).reshape(-1,1)
    ax.imshow(gradient, aspect='auto', cmap=cmap, origin='lower', extent=[times[0], times[-1], ymin, ymax])
    ax.plot(times, densities, color='black', linewidth=2)
    x_text = times[0] - 0.02*(times[-1]-times[0])
    for i, lower in enumerate(REG_THRESH):
        upper = REG_THRESH[i+1] if i+1 < len(REG_THRESH) else ymax
        y_mid = (lower + upper)/2
        ax.text(x_text, y_mid, REG_LABELS[i], va='center', ha='right', fontsize=10, weight='bold', backgroundcolor='white', alpha=0.7)
    ax.set_xlim(x_text, times[-1])
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Crowd Density (people per pixel area)")
    ax.set_title("Crowd Density Over Time with Risk Zones")
    plt.tight_layout()
    plt.close(fig)

    # Aggregate metrics per second
    metrics_per_second = []
    for sec in range(int(times[-1]) + 1):
        frames_in_second = [i for i, t in enumerate(times) if int(t) == sec]
        if frames_in_second:
            avg_density = np.mean([densities[i] for i in frames_in_second])
            avg_people = np.mean([people_counts[i] for i in frames_in_second])
            # For risk and status, take the most frequent value in the second
            most_frequent_risk = max(set([risk_levels[i] for i in frames_in_second]), key=[risk_levels[i] for i in frames_in_second].count)
            most_frequent_status = max(set([status_levels[i] for i in frames_in_second]), key=[status_levels[i] for i in frames_in_second].count)
            metrics_per_second.append({
                "second": sec,
                "average_density": avg_density,
                "average_people": avg_people,
                "risk": most_frequent_risk,
                "status": most_frequent_status
            })
        else:
             metrics_per_second.append({
                "second": sec,
                "average_density": 0,
                "average_people": 0,
                "risk": "Low",
                "status": "Free Flowing"
            })


    return out_path, fig, metrics_per_second

iface = gr.Interface(
    fn=process_video,
    inputs=[
        gr.Video(label="Upload Video"),
        gr.Slider(2, 10, value=2, step=1, label="Frame Skip"),
        gr.Slider(1, CPU_CORES, value=MAX_WORKERS, step=1, label="Max Workers")
    ],
    outputs=[
        gr.Video(label="Annotated Video"),
        gr.Plot(label="Crowd Density Over Time with Risk Zones"),
        gr.JSON(label="Metrics Per Second")
    ],
    title="Drishti AI"
)

if __name__ == "__main__":
    iface.launch(debug=True, server_name='0.0.0.0')