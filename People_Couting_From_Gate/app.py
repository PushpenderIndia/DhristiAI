import gradio as gr
import cv2
import json
import tempfile
from ultralytics import YOLO
from collections import defaultdict

model = YOLO('yolov8s.pt')

def process_video(video_path: str, max_thresh: int):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    out = cv2.VideoWriter(out_temp.name, fourcc, fps, (width, height))

    per_sec = defaultdict(int)
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1
        sec = int(frame_idx / fps)

        results = model(frame, conf=0.3)[0]
        cnt = sum(1 for cls in results.boxes.cls if int(cls) == 0)
        per_sec[sec] = max(per_sec[sec], cnt)

        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            if int(cls) == 0:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

        if cnt >= max_thresh:
            text = f"THRESHOLD EXCEEDED! Count={cnt}"
            cv2.putText(frame, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

        out.write(frame)

    cap.release()
    out.release()

    metrics = [{"second": s, "count": per_sec[s]} for s in sorted(per_sec)]
    json_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    with open(json_temp.name, "w") as jf:
        json.dump({"metrics": metrics}, jf)

    return out_temp.name, json_temp.name

with gr.Blocks() as demo:
    gr.Markdown("### People Counter with Threshold Alert")
    vid_in = gr.File(file_types=["video"], label="Upload video")
    threshold_input = gr.Number(value=5, label="Max threshold count", precision=0)
    out_vid = gr.Video(label="Processed Video", autoplay=True)
    out_json = gr.File(label="Metrics JSON")
    btn = gr.Button("Run")

    def run_fn(uploaded, max_t):
        if uploaded is None:
            return None, None
        outv, metrics = process_video(uploaded.name, int(max_t))
        return outv, metrics

    btn.click(run_fn, inputs=[vid_in, threshold_input], outputs=[out_vid, out_json])

demo.launch()
