import React from "react";

const SignLanguage = () => {
  return (
    <div className="p-6 text-center">
      <h2 className="text-3xl font-bold">Sign Language Recognition</h2>
      <p className="mt-4 text-gray-700">Use your camera to interpret sign language gestures.</p>
      <button className="mt-6 px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition">
        Start Recognition
      </button>
    </div>
  );
};

export default SignLanguage;
