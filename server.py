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
origins = [
    "http://localhost:3000",  # Frontend local development
    "https://your-frontend-domain.com",  # Replace with your actual frontend URL
    # Add other allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],     # Allow all HTTP methods
    allow_headers=["*"],     # Allow all headers
)

# Load Coqui TTS Model
# It's efficient to load the model once at startup
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")

# Define request schema using Pydantic
class SynthesizeRequest(BaseModel):
    text: str

# Maximum allowed text length to prevent large requests
MAX_TEXT_LENGTH = 1000  # Adjust as needed

@app.post("/synthesize")
async def synthesize_text(request: SynthesizeRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")
    
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=413,
            detail=f"Text too long. Maximum allowed length is {MAX_TEXT_LENGTH} characters."
        )
    
    try:
        # Create a unique temporary file for each request
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            output_path = tmp_file.name
        
        # Synthesize speech and save to the temporary file
        tts.tts_to_file(text=text, file_path=output_path)
        
        # Return the audio file as a response
        return FileResponse(
            path=output_path,
            media_type="audio/wav",
            filename="speech.wav"
        )
    except Exception as e:
        # Log the exception details (you might want to use a logging framework)
        print(f"Error during synthesis: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during synthesis.")
    finally:
        # Schedule the temporary file for deletion
        # In production, consider using a background task or cron job to clean up old files
        if os.path.exists(output_path):
            os.remove(output_path)

@app.get("/")
def home():
    return {"message": "Coqui TTS Server is running!"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
