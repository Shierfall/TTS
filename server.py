from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from TTS.api import TTS
import os

app = FastAPI()

# Load Coqui TTS Model
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")  # Use a small model for better performance

# Ensure output directory exists
output_dir = "audio_outputs"
os.makedirs(output_dir, exist_ok=True)

@app.post("/synthesize")
def synthesize_text(text: str = Form(...)):
    output_path = os.path.join(output_dir, "output.wav")
    tts.tts_to_file(text=text, file_path=output_path)
    return FileResponse(output_path, media_type="audio/wav", filename="speech.wav")

@app.get("/")
def home():
    return {"message": "Coqui TTS Server is running on Render!"}
