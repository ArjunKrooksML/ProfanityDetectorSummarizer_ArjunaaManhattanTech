import easyocr

reader = easyocr.Reader(['en'])

def load_prolist(lang_code):
    try:
        with open(f'profanity_lists/{lang_code}.txt', 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def protext(frames_with_timestamps, lang_code='hindi'):
    profanity_words = load_prolist(lang_code)
    flagged_frames = []

    for frame_path, timestamp in frames_with_timestamps:
        text_data = reader.readtext(frame_path, detail=0)
        matches = [w for w in profanity_words if any(w in t.lower() for t in text_data)]
        if matches:
            flagged_frames.append({
                "frame": frame_path,
                "timestamp": timestamp,
                "matches": matches
            })
    return flagged_frames
