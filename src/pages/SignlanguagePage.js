import React from "react";

const SignLanguagePage = ({ darkMode }) => {
  return (
    <div className={`app-container ${darkMode ? "dark-mode" : "light-mode"}`}>
      <div className="box-container">
        <h2>Sign Language Detection</h2>
        <p>Upload an image or use webcam to detect sign language.</p>
        <button>Upload Image</button>
        <button>Start Webcam</button>
      </div>
    </div>
  );
};

export default SignLanguagePage;
