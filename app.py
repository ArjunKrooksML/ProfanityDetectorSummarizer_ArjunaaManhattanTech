import streamlit as st
from video_structure import extractinfo, sample_frames, extract_audio
from nsfw_detection import detect_nsfw
from audio_analysis import transcribe, abusedet
from moderation import sum_mist
from ocr import frameocr  # You’ll need this file
from directory import createdirectories

# Setup folders
createdirectories()

# Streamlit UI
st.title("Content Censoring/Moderation Tool (VOSK, Tesseract, Streamlit, Mistral)")

uploaded_video = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

if uploaded_video is not None:
    with open("temp/input_video.mp4", "wb") as f:
        f.write(uploaded_video.read())

    st.video("temp/input_video.mp4")

    st.info("Extracting video info...")
    fps, duration, resolution = extractinfo("temp/input_video.mp4")
    st.success(f"Video FPS: {fps}, Duration: {duration:.2f}s, Resolution: {resolution}")

    st.info("Sampling frames and extracting audio...")
    frames = sample_frames("temp/input_video.mp4")
    audio_path = extract_audio("temp/input_video.mp4")

    st.info("Running NSFW detection...")
    nsfw_results = detect_nsfw(frames)
    if nsfw_results:
        for item in nsfw_results:
            st.warning(f"NSFW at {item['timestamp']}s: {item['label']} (score: {item['score']})")
    else:
        st.success("No NSFW content detected.")

    st.info("Transcribing audio and checking for abuse...")
    transcript, segments = transcribe(audio_path)
    abusive_segments = []
    for s in segments:
        abuse_scores = abusedet(s['text'])
        if any(score > 0.7 for score in abuse_scores.values()):
            abusive_segments.append({
                "start": s['start'],
                "end": s['end'],
                "text": s['text'],
                "scores": abuse_scores
            })

    if abusive_segments:
        for a in abusive_segments:
            st.error(f"Abuse between {a['start']}s - {a['end']}s: {a['text']}")
    else:
        st.success("No abusive language detected in audio.")

    st.info("Running OCR on video frames...")
    ocr_results = frameocr(frames)
    if ocr_results:
        st.warning("Detected on-screen text:")
        for item in ocr_results:
            st.write(f"At {item['timestamp']}s: \"{item['text']}\"")
    else:
        st.success("No visible text detected.")

    st.info("Generating summary report using Mistral...")
    summary = sum_mist(nsfw_results, abusive_segments, ocr_results)
    st.subheader("Final Moderation Summary")
    st.markdown(summary)
