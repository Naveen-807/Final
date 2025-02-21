import React, { useState, useRef } from "react";
import axios from 'axios';
import Webcam from 'react-webcam';

const SignLanguagePage = ({ darkMode }) => {
  const [detections, setDetections] = useState([]);
  const [mode, setMode] = useState(null);
  const webcamRef = useRef(null);
  const fileInputRef = useRef(null);

  const detectGesture = async (imageSource) => {
    try {
      let base64Image;
      
      // Handle different image sources
      if (mode === 'webcam') {
        const imageSrc = webcamRef.current.getScreenshot();
        base64Image = imageSrc.split(',')[1];
      } else if (mode === 'upload' && imageSource) {
        // Convert uploaded file to base64
        const reader = new FileReader();
        reader.readAsDataURL(imageSource);
        base64Image = await new Promise((resolve) => {
          reader.onloadend = () => {
            resolve(reader.result.split(',')[1]);
          };
        });
      }

      // Send to backend
      const response = await axios.post('/detect_gesture', {
        image: base64Image
      });
      
      // Update detections
      if (response.data.success) {
        setDetections(response.data.detections);
      }
    } catch (error) {
      console.error('Gesture detection error:', error);
    }
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setMode('upload');
      detectGesture(file);
    }
  };

  const startWebcam = () => {
    setMode('webcam');
  };

  return (
    <div className={`app-container ${darkMode ? "dark-mode" : "light-mode"}`}>
      <div className="box-container">
        <h2>Sign Language Detection</h2>
        <p>Upload an image or use webcam to detect sign language.</p>
        
        {/* Image Upload Button */}
        <input 
          type="file" 
          ref={fileInputRef}
          style={{ display: 'none' }}
          accept="image/*"
          onChange={handleImageUpload}
        />
        <button onClick={() => fileInputRef.current.click()}>
          Upload Image
        </button>
        
        {/* Webcam Button */}
        <button onClick={startWebcam}>
          Start Webcam
        </button>

        {/* Webcam Component */}
        {mode === 'webcam' && (
          <div className="webcam-container">
            <Webcam
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              videoConstraints={{
                width: 640,
                height: 480
              }}
            />
            <button onClick={() => detectGesture()}>
              Detect Gesture
            </button>
          </div>
        )}

        {/* Detections Display */}
        {detections.length > 0 && (
          <div className="detections-container">
            <h3>Detected Gestures:</h3>
            {detections.map((detection, index) => (
              <div key={index} className="detection">
                <span>Gesture: {detection.class}</span>
                <span>Confidence: {detection.confidence.toFixed(2)}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SignLanguagePage;