import os
import wave
import json
from vosk import Model, KaldiRecognizer
from detoxify import Detoxify

model = Model("models/vosk-model-small-en-us-0.15")

def transcribe(audio_path):
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    full_text = ""
    segments = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            if res.get("text"):
                segments.append({"start": None, "end": None, "text": res["text"]})
                full_text += res["text"] + " "

    final_res = json.loads(rec.FinalResult())
    if final_res.get("text"):
        segments.append({"start": None, "end": None, "text": final_res["text"]})
        full_text += final_res["text"]

    return full_text.strip(), segments

def abusedet(text):
    scores = Detoxify("original").predict(text)
    return scores
