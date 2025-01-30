import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from TTS.api import TTS
import tempfile
import soundfile as sf
from pydantic import BaseModel

app = FastAPI()

# ✅ Enable CORS (Allows frontend to access the API)
origins = ["*"]  # Allow all origins (update if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request schema
class SynthesizeRequest(BaseModel):
    text: str

MAX_TEXT_LENGTH = 1000  # Prevent large requests

@app.post("/synthesize")
async def synthesize_text(request: SynthesizeRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(status_code=413, detail=f"Max length is {MAX_TEXT_LENGTH} characters.")

    try:
        tts = TTS("tts_models/en/ljspeech/fast_pitch")

        # Create temp file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_path = tmp_file.name

        # Generate speech
        tts.tts_to_file(text=text, file_path=output_path)

        # ✅ Debug: Check if the file is valid
        data, samplerate = sf.read(output_path)
        print(f"✅ WAV File Generated: {output_path}, Duration: {len(data) / samplerate:.2f} sec")

        # ✅ Read file and return as binary response
        with open(output_path, "rb") as audio_file:
            return Response(audio_file.read(), media_type="audio/wav")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error during synthesis.")

@app.get("/")
def home():
    return {"message": "Coqui TTS Server is running!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # ✅ Render uses dynamic ports
    print(f"🚀 FastAPI running on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
