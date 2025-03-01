import React, { useState } from "react";
import "./toto.css"
export default function TextToSignPage() {
  const [word, setWord] = useState("");
  const [gifUrl, setGifUrl] = useState("");

  const fetchGif = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/get_gif?word=${word}`);
      const data = await response.json();
      if (data.gif_url) {
        setGifUrl(data.gif_url);
      } else {
        alert("GIF not found!");
        setGifUrl("");
      }
    } catch (error) {
      console.error("Error fetching GIF:", error);
    }
  };

  return (
    <div>
      <h1>Text to Sign language learning</h1>
      <input
        type="text"
        placeholder="Enter a word..."
        value={word}
        onChange={(e) => setWord(e.target.value)}
      />
      <button onClick={fetchGif}>Get GIF</button>
      {gifUrl && <img src={gifUrl} alt="GIF" />}
    </div>
  );
}

