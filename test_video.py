import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pyttsx3
import os

def create_video_with_text_and_audio(text, output_video="output_video.avi", output_audio="output_audio.wav"):
    width, height = 1280, 720
    fps = 24
    duration_sec = 5
    total_frames = fps * duration_sec

    # Font setup (try a truetype font path, fallback to default)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)  # Adjust font size and path if needed
    except IOError:
        font = ImageFont.load_default()

    # Create frames
    frames = []
    for _ in range(total_frames):
        img = Image.new("RGB", (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Get text size and position
        text_size = draw.textbbox((0, 0), text, font=font)
        text_width = text_size[2] - text_size[0]
        text_height = text_size[3] - text_size[1]
        text_position = ((width - text_width) // 2, (height - text_height) // 2)

        # Draw the text
        draw.text(text_position, text, font=font, fill=(255, 255, 255))

        # Convert to OpenCV format
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        frames.append(frame)

    # Write video
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*"XVID"), fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()
    print(f"[+] Video saved as {output_video}")

    # Generate audio using pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.save_to_file(text, output_audio)
    engine.runAndWait()
    print(f"[+] Audio saved as {output_audio}")

    # Merge audio and video using ffmpeg (must be installed)
    final_output = "final_output.mp4"
    os.system(f"ffmpeg -y -i {output_video} -i {output_audio} -c:v copy -c:a aac -strict experimental {final_output}")
    print(f"[+] Final video with audio saved as {final_output}")


# Example
if __name__ == "__main__":
    create_video_with_text_and_audio("You are a fucking pig")
