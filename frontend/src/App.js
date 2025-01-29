import React, { useState } from "react";
import axios from "axios";

function App() {
  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const synthesizeSpeech = async () => {
    if (!text) return;
    setLoading(true);
    try {
      const response = await axios.post(
        "https://your-app-name.onrender.com/synthesize",
        new URLSearchParams({ text })
      );
      setAudioUrl(response.request.responseURL);
    } catch (error) {
      console.error("Error generating speech:", error);
    }
    setLoading(false);
  };

  return (
    <div style={{ textAlign: "center", padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2>Text-to-Speech Generator</h2>
      <textarea
        rows="4"
        cols="50"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text..."
      />
      <br />
      <button onClick={synthesizeSpeech} disabled={loading}>
        {loading ? "Generating..." : "Convert to Speech"}
      </button>
      {audioUrl && (
        <div>
          <h3>Generated Speech:</h3>
          <audio controls src={audioUrl}></audio>
        </div>
      )}
    </div>
  );
}

export default App;
