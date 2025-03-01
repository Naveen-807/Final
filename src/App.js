import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, NavLink } from "react-router-dom";
import { 
  FaHome, 
  FaRobot, 
  FaSignLanguage, 
  FaCode,
  FaVolumeUp, // Text to Speech icon
  FaHeartbeat  // Health Bot icon
} from "react-icons/fa";
import "./App.css";

// Import your page components
import Home from "./pages/Home";
import ChatbotPage from "./pages/ChatbotPage";
import SignLanguagePage from "./pages/SignlanguagePage";
import TextToSignPage from "./pages/TextToSignPage";


// Color Palette
const COLORS = {
  background: "#121212",
  navBackground: "rgba(18,18,18,0.95)",
  text: "#e0e0e0",
  accent: "#bb86fc",
  accentVariant: "#03dac6",
  surface: "#1e1e1e",
};

// NotFound Component
const NotFound = () => (
  <div style={{ textAlign: "center", padding: "50px", color: COLORS.accent }}>
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
  </div>
);

function App() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Navigation link styles
  const navLinkStyle = ({ isActive }) => ({
    display: "flex",
    alignItems: "center",
    gap: "10px",
    padding: "10px 15px",
    borderRadius: "8px",
    transition: "all 0.3s ease",
    color: isActive ? COLORS.background : COLORS.text,
    background: isActive ? COLORS.accent : "transparent",
    textDecoration: "none",
    fontWeight: "bold",
  });

  return (
    <Router>
      <div
        style={{
          minHeight: "100vh",
          background: `linear-gradient(to right, ${COLORS.background}, #1a1a1a)`,
          color: COLORS.text,
          fontFamily: "'Roboto Mono', monospace",
        }}
      >
        {/* Cyberpunk Navigation Bar */}
        <nav
          style={{
            background: COLORS.navBackground,
            backdropFilter: "blur(10px)",
            boxShadow: "0 4px 6px rgba(0,0,0,0.2)",
            position: "sticky",
            top: 0,
            zIndex: 1000,
            borderBottom: `1px solid ${COLORS.accent}`,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              maxWidth: "1200px",
              margin: "0 auto",
              padding: "15px 20px",
            }}
          >
            {/* Logo */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "10px",
                fontSize: "1.5rem",
                fontWeight: "bold",
                color: COLORS.accent,
              }}
            >
              <FaCode style={{ color: COLORS.accentVariant }} />
              AccessTech
            </div>

            {/* System Time */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "15px",
                color: COLORS.accentVariant,
              }}
            >
              {time.toLocaleTimeString()}
            </div>

            {/* Navigation Links */}
            <div style={{ display: "flex", gap: "1rem" }}>
              <NavLink to="/" style={navLinkStyle}>
                <FaHome /> Home
              </NavLink>
              <NavLink to="/chatbot" style={navLinkStyle}>
                <FaRobot /> Chatbot
              </NavLink>
              <NavLink to="/sign-language" style={navLinkStyle}>
                <FaSignLanguage /> Sign Language
              </NavLink>
              <NavLink to="http://localhost:8501" style={navLinkStyle}>
                <FaHeartbeat /> TextToSpeech 
              </NavLink>
              <NavLink to="http://localhost:8502" style={navLinkStyle}>
                <FaHeartbeat /> Health Bot
              </NavLink>
              <NavLink to="/texttosign" style={navLinkStyle}>
                <FaHeartbeat /> Text to Sign 
              </NavLink>
              
            </div>
          </div>
        </nav>

        {/* Page Content */}
        <div
          style={{
            maxWidth: "1200px",
            margin: "0 auto",
            padding: "1.5rem",
            background: COLORS.surface,
            minHeight: "calc(100vh - 70px)",
            boxShadow: "0 0 30px rgba(0,0,0,0.3)",
          }}
        >
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chatbot" element={<ChatbotPage />} />
            <Route path="/sign-language" element={<SignLanguagePage />} />
            <Route path="/texttosign" element={<TextToSignPage />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
