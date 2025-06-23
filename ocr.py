from PIL import Image
import pytesseract

def frameocr(frame_paths):   
    ocr_results = []
    for frame_path, timestamp in frame_paths:
        try:
            text = pytesseract.image_to_string(Image.open(frame_path)).strip()
            if text:
                ocr_results.append({
                    "timestamp": round(timestamp, 2),
                    "text": text
                })
        except Exception as e:
            print(f"Error reading {frame_path}: {e}")
            continue

    return ocr_results