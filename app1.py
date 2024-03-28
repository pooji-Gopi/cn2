from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import shutil
import speech_recognition as sr
from moviepy.editor import VideoFileClip

app = FastAPI()

class VideoRequest(BaseModel):
    video: UploadFile

@app.post("/extract-text")
async def extract_text(video: UploadFile = File(...)):
    try:
        # Save the uploaded video file
        video_path = "uploaded_video.mp4"
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)

        # Convert video to audio
        audio_path = "temp_audio.wav"
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)

        # Transcribe audio to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)

        # Perform speech recognition using Google
        text = recognizer.recognize_google(audio)

        # Write recognized text to a file
        with open('recognized_text.txt', mode='w') as file:
            file.write(text)

        return {"text": text}
    
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}
