import { useState } from "react";
import axios from "axios";
import "./toto.css"
const TextToSpeech = () => {
  const [text, setText] = useState("");
  const [gifUrl, setGifUrl] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = async (e) => {
    const inputText = e.target.value.trim().toUpperCase(); // Convert to uppercase
    setText(inputText);

    if (inputText) {
      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/get_gif?word=${inputText}`
        );
        setGifUrl(`http://127.0.0.1:5000${response.data.gif_url}`);
        setError(null);
      } catch (err) {
        setGifUrl(null);
        setError("GIF not found.");
      }
    } else {
      setGifUrl(null);
      setError(null);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h2 className="text-2xl font-bold mb-4">Enter a Word to Display GIF</h2>
      <input
        type="text"
        placeholder="Type a word..."
        value={text}
        onChange={handleChange}
        className="border p-2 rounded-md text-lg"
      />
      <div className="mt-4">
        {gifUrl && <img src={gifUrl} alt="GIF" className="w-64" />}
        {error && <p className="text-red-500">{error}</p>}
      </div>
    </div>
  );
};

export default TextToSpeech;