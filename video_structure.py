import cv2
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import uuid
import subprocess
import datetime
import pytesseract
from PIL import Image

def extractinfo(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    resolution = (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )
    cap.release()
    return fps, duration, resolution

def sample_frames(video_path, frame_gap=2):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * frame_gap)
    frame_paths = []

    frame_count = 0
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_filename = f"temp/frames/frame_{saved_count}_{uuid.uuid4().hex}.jpg"
            cv2.imwrite(frame_filename, frame)
            frame_paths.append((frame_filename, frame_count / fps))
            saved_count += 1

        frame_count += 1

    cap.release()
    return frame_paths



def extract_audio(video_path, output_dir="temp/audio"):    
    os.makedirs(output_dir, exist_ok=True)  
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"audio_{timestamp}.wav")  
    command = [
        "ffmpeg", "-y",  # overwrite without asking (safe here since file name is unique)
        "-i", video_path,
        "-vn",                  # remove video
        "-acodec", "pcm_s16le", # uncompressed WAV
        "-ar", "16000",         # sample rate 16kHz
        "-ac", "1",             # mono
        output_path
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to extract audio: {e}")
        return None
