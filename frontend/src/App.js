import React, { useState } from "react";
import axios from "axios";

function App() {
  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const synthesizeSpeech = async () => {
    if (!text.trim()) {
      setError("Please enter some text.");
      return;
    }

    setLoading(true);
    setError(null);
    setAudioUrl(null);

    try {
      const response = await axios.post(
        "https://tts-l97q.onrender.com/synthesize", // Corrected Endpoint
        { text }, // Sending JSON payload
        {
          responseType: "blob", // Expecting binary data
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      // Create a Blob from the response
      const audioBlob = new Blob([response.data], { type: "audio/wav" });
      // Generate a URL for the Blob
      const url = URL.createObjectURL(audioBlob);
      setAudioUrl(url);
    } catch (error) {
      console.error("Error generating speech:", error);
      setError("Failed to generate speech. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Text-to-Speech Generator</h2>
      <textarea
        style={styles.textarea}
        rows="4"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text..."
      />
      <br />
      <button onClick={synthesizeSpeech} disabled={loading} style={styles.button}>
        {loading ? "Generating..." : "Convert to Speech"}
      </button>
      {error && <p style={styles.error}>{error}</p>}
      {audioUrl && (
        <div style={styles.audioContainer}>
          <h3>Generated Speech:</h3>
          <audio controls src={audioUrl}></audio>
          <br />
          <a href={audioUrl} download="speech.wav">
            <button style={styles.downloadButton}>Download Audio</button>
          </a>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
    maxWidth: "600px",
    margin: "0 auto",
  },
  textarea: {
    width: "100%",
    padding: "10px",
    fontSize: "16px",
    boxSizing: "border-box",
  },
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    marginTop: "10px",
    cursor: "pointer",
  },
  downloadButton: {
    padding: "8px 16px",
    fontSize: "14px",
    marginTop: "10px",
    cursor: "pointer",
  },
  error: {
    color: "red",
    marginTop: "10px",
  },
  audioContainer: {
    marginTop: "20px",
  },
};

export default App;
