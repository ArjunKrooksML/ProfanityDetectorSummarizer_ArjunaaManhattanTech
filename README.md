# ProfanityDetectorSummarizer_ArjunaaManhattanTech
Profanity detector and summarizer in Videos built using VOSK 'en' and Mistral 7B. 

Install WSL dependencies:
sudo apt install ffmpeg tesseract-ocr espeak-ng -y

pip install -r requirements.txt

This Streamlit application performs automated moderation on short videos by analyzing:
-NSFW visual content using NudeNet
-Abusive language in audio using VOSK and Detoxify
-On-screen text using Tesseract OCR
-Final moderation summary generated using Mistral-7B via Hugging Face

Features:
-Upload videos in .mp4, .mov, or .avi format
-Extracts frames and audio
-Detects and timestamps NSFW visual elements
-Transcribes audio and identifies abusive speech
-Extracts and analyzes on-screen text

Summarizes all detections using the Mistral 7B model in Gated Access

