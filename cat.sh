curl -X 'POST' \
  'https://c331-35-186-145-193.ngrok-free.app/synthesize' \
  -H 'Content-Type: application/json' \
  -d '{"text": "Hello, this is a test"}' \
  --output test_audio.wav
