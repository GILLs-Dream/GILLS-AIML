import cv2
import os

def extract_frames(video_path, output_dir, interval_sec=1):
    os.makedirs(output_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)
    count = 0
    saved_count = 0

    while True:
        success, frame = vidcap.read()
        if not success:
            break
        if count % frame_interval == 0:
            frame_filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_count += 1
        count += 1

    vidcap.release()