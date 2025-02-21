import React, { useState, useEffect } from 'react';
import './HandGestureRecognizer.css';

function App() {
  const [currentGesture, setCurrentGesture] = useState({ gesture: 'No gesture detected', confidence: 0 });
  const [supportedGestures, setSupportedGestures] = useState([]);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Check camera status on component mount
  useEffect(() => {
    checkCameraStatus();
  }, []);

  const checkCameraStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/camera/status');
      const data = await response.json();
      setIsCameraOn(data.is_running);
    } catch (error) {
      console.error('Error checking camera status:', error);
    }
  };

  const toggleCamera = async () => {
    setIsLoading(true);
    try {
      const endpoint = isCameraOn ? '/camera/stop' : '/camera/start';
      const response = await fetch(`http://localhost:5000${endpoint}`, {
        method: 'POST'
      });
      const data = await response.json();
      
      if (data.success) {
        setIsCameraOn(!isCameraOn);
        if (!isCameraOn) {
          // Start fetching gestures when camera is turned on
          startGestureFetching();
        }
      } else {
        console.error('Failed to toggle camera');
      }
    } catch (error) {
      console.error('Error toggling camera:', error);
    }
    setIsLoading(false);
  };

  const startGestureFetching = () => {
    // Fetch current gesture periodically when camera is on
    const fetchGesture = async () => {
      if (!isCameraOn) return;
      
      try {
        const response = await fetch('http://localhost:5000/current_gesture');
        const data = await response.json();
        setCurrentGesture(data);
      } catch (error) {
        console.error('Error fetching gesture:', error);
      }
    };

    // Update gesture every 500ms
    const intervalId = setInterval(fetchGesture, 500);
    return () => clearInterval(intervalId);
  };

  // Fetch supported gestures once on component mount
  useEffect(() => {
    const fetchSupportedGestures = async () => {
      try {
        const response = await fetch('http://localhost:5000/supported_gestures');
        const data = await response.json();
        setSupportedGestures(data.gestures);
      } catch (error) {
        console.error('Error fetching supported gestures:', error);
      }
    };

    fetchSupportedGestures();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Real-time Sign Language Recognition</h1>
        <button 
          className={`camera-toggle ${isCameraOn ? 'on' : 'off'}`}
          onClick={toggleCamera}
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : (isCameraOn ? 'Turn Camera Off' : 'Turn Camera On')}
        </button>
      </header>

      <main className="App-main">
        <div className="video-container">
          {isCameraOn ? (
            <img 
              src="http://localhost:5000/video_feed" 
              alt="Video feed"
              className="video-feed"
            />
          ) : (
            <div className="video-placeholder">
              <p>Camera is turned off</p>
              <p>Click the button above to start</p>
            </div>
          )}
          
          <div className="current-gesture">
            <h2>Current Gesture</h2>
            <p className="gesture-name">{currentGesture.gesture}</p>
            <p className="confidence">
              Confidence: {(currentGesture.confidence * 100).toFixed(2)}%
            </p>
          </div>
        </div>

        <div className="gestures-list">
          <h2>Supported Gestures</h2>
          <div className="gestures-grid">
            {supportedGestures.map((gesture, index) => (
              <div key={index} className="gesture-card">
                <h3>{gesture.name}</h3>
                <p>{gesture.description}</p>
                <p><strong>Meaning:</strong> {gesture.meaning}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;