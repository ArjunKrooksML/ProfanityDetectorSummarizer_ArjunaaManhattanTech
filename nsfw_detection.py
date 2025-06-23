from nudenet import NudeDetector

detector = NudeDetector()

def detect_nsfw(frames_with_timestamps, threshold=0.8):
    results = []
    for frame_path, timestamp in frames_with_timestamps:
        detections = detector.detect(frame_path)
        for item in detections:
            if item['score'] >= threshold:
                results.append({
                    "frame": frame_path,
                    "timestamp": round(timestamp, 2),
                    "score": round(item['score'], 3),
                    "label": item['label'],
                    "box": item['box']
                })
    return results
