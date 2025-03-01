import React, { useEffect, useState } from "react";
import { createDirectLine } from "botframework-webchat";
import { motion } from "framer-motion";
import ReactWebChat from "botframework-webchat";

const HealthBot = () => {
  const [directLine, setDirectLine] = useState(null);

  useEffect(() => {
    fetch("/api/get_token")
      .then((res) => res.json())
      .then((data) => {
        if (data.token) {
          setDirectLine(createDirectLine({ token: data.token }));
        } else {
          console.error("Failed to fetch Direct Line token:", data);
        }
      })
      .catch((err) => console.error("Error fetching Direct Line token:", err));
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex justify-center items-center h-screen bg-gray-900 text-white"
    >
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 className="text-lg font-bold text-center mb-4">HealthBot</h2>
        {directLine ? (
          <ReactWebChat directLine={directLine} className="bg-white text-black p-4 rounded" />
        ) : (
          <p>Loading chatbot...</p>
        )}
      </div>
    </motion.div>
  );
};

export default HealthBot;
