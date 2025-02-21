import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, NavLink } from "react-router-dom";
import { 
  FaHome, 
  FaRobot, 
  FaSignLanguage, 
  FaCode,
  FaTerminal
} from 'react-icons/fa';
import "./App.css";

// Import your page components
import Home from "./pages/Home";
import ChatbotPage from "./pages/ChatbotPage";
import SignLanguagePage from "./pages/SignlanguagePage";

// Color Palette
const COLORS = {
  background: '#121212',
  navBackground: 'rgba(18,18,18,0.95)',
  text: '#e0e0e0',
  accent: '#bb86fc',
  accentVariant: '#03dac6',
  surface: '#1e1e1e'
};

// NotFound Component
const NotFound = () => {
  return (
    <div 
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        background: `linear-gradient(135deg, ${COLORS.background} 0%, #1f1f1f 100%)`,
        color: COLORS.text,
        fontFamily: "'Roboto Mono', monospace",
        perspective: '1000px'
      }}
    >
      <div 
        style={{
          textAlign: 'center',
          transform: 'rotateX(10deg)',
          transition: 'all 0.3s ease'
        }}
      >
        <h1 
          style={{ 
            fontSize: '10rem', 
            fontWeight: 'bold', 
            color: COLORS.accent,
            textShadow: `0 0 20px ${COLORS.accent}`,
            marginBottom: '1rem'
          }}
        >
          404
        </h1>
        <p 
          style={{ 
            fontSize: '1.5rem', 
            color: COLORS.accentVariant,
            marginBottom: '2rem'
          }}
        >
          System Error: Page Not Found
        </p>
        <NavLink 
          to="/" 
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '10px',
            padding: '12px 24px',
            background: COLORS.accent,
            color: COLORS.background,
            borderRadius: '8px',
            textDecoration: 'none',
            fontWeight: 'bold',
            transition: 'all 0.3s ease',
            boxShadow: `0 0 15px ${COLORS.accent}`,
            transform: 'translateZ(50px)',
            position: 'relative',
            overflow: 'hidden'
          }}
          onMouseEnter={(e) => {
            e.target.style.transform = 'scale(1.05) translateZ(50px)';
            e.target.style.boxShadow = `0 0 25px ${COLORS.accent}`;
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = 'scale(1) translateZ(50px)';
            e.target.style.boxShadow = `0 0 15px ${COLORS.accent}`;
          }}
        >
          <FaTerminal /> Return to Main System
        </NavLink>
      </div>
    </div>
  );
};

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [time, setTime] = useState(new Date());

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  // Navigation link styles
  const navLinkStyle = ({ isActive }) => ({
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '10px 15px',
    borderRadius: '8px',
    transition: 'all 0.3s ease',
    color: isActive ? COLORS.background : COLORS.text,
    background: isActive ? COLORS.accent : 'transparent',
    textDecoration: 'none',
    fontWeight: 'bold',
    transform: 'perspective(500px) translateZ(0)',
    position: 'relative',
    overflow: 'hidden'
  });

  return (
    <Router>
      <div 
        style={{
          minHeight: '100vh',
          background: `linear-gradient(to right, ${COLORS.background}, #1a1a1a)`,
          color: COLORS.text,
          fontFamily: "'Roboto Mono', monospace"
        }}
      >
        {/* Cyberpunk Navigation Bar */}
        <nav 
          style={{
            background: COLORS.navBackground,
            backdropFilter: 'blur(10px)',
            boxShadow: '0 4px 6px rgba(0,0,0,0.2)',
            position: 'sticky',
            top: 0,
            zIndex: 1000,
            borderBottom: `1px solid ${COLORS.accent}`
          }}
        >
          <div 
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              maxWidth: '1200px',
              margin: '0 auto',
              padding: '15px 20px'
            }}
          >
            {/* Logo with Cyberpunk Style */}
            <div 
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                fontSize: '1.5rem',
                fontWeight: 'bold',
                color: COLORS.accent
              }}
            >
              <FaCode style={{ color: COLORS.accentVariant }} />
              AccessTech
            </div>

            {/* System Time and Status */}
            <div 
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '15px',
                color: COLORS.accentVariant
              }}
            >
              {time.toLocaleTimeString()}
            </div>

            {/* Desktop Navigation */}
            <div 
              style={{
                display: 'flex',
                gap: '1rem'
              }}
            >
              <NavLink to="/" style={navLinkStyle}>
                <FaHome /> Home
              </NavLink>
              <NavLink to="/chatbot" style={navLinkStyle}>
                <FaRobot /> Chatbot
              </NavLink>
              <NavLink to="/sign-language" style={navLinkStyle}>
                <FaSignLanguage /> Sign Language
              </NavLink>
            </div>
          </div>
        </nav>

        {/* Page Content */}
        <div 
          style={{
            maxWidth: '1200px',
            margin: '0 auto',
            padding: '1.5rem',
            background: COLORS.surface,
            minHeight: 'calc(100vh - 70px)',
            boxShadow: '0 0 30px rgba(0,0,0,0.3)'
          }}
        >
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/Chatbot" element={<ChatbotPage />} />
            <Route path="/Sign-Language" element={<SignLanguagePage />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;