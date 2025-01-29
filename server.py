import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from TTS.api import TTS
import tempfile
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
origins = ["http://localhost:3000", "https://your-frontend-domain.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Print debug line
print("Starting server and loading TTS model...")

# Load Coqui TTS Model (use a smaller model if needed)
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
print("TTS model loaded.")

class SynthesizeRequest(BaseModel):
    text: str

MAX_TEXT_LENGTH = 1000

@app.post("/synthesize")
async def synthesize_text(request: SynthesizeRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(status_code=413, detail=f"Max length is {MAX_TEXT_LENGTH} characters.")

    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_path = tmp_file.name
        tts.tts_to_file(text=text, file_path=output_path)
        return FileResponse(path=output_path, media_type="audio/wav", filename="speech.wav")
    except Exception as e:
        print(f"Error during synthesis: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during synthesis.")

@app.get("/")
def home():
    return {"message": "Coqui TTS Server is running!"}
