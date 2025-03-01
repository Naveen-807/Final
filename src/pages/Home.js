import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { 
  FaRobot, 
  FaHandshake, 
  FaMoon, 
  FaSun, 
  FaArrowRight,
  FaVolumeUp,  // Icon for Text to Speech
  FaSignLanguage,  // Icon for Text to Sign
  FaHeartbeat  // Icon for Healthbot
} from 'react-icons/fa';

const Home = () => {
  const [darkMode, setDarkMode] = useState(false);
  const navigate = useNavigate();

  // Dark mode toggle
  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    localStorage.setItem('darkMode', JSON.stringify(newDarkMode));
    document.body.classList.toggle('dark-mode');
  };

  // Load dark mode preference on component mount
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode) {
      const isDarkMode = JSON.parse(savedDarkMode);
      setDarkMode(isDarkMode);
      document.body.classList.toggle('dark-mode', isDarkMode);
    }
  }, []);

  // Styles
  const styles = {
    container: {
      fontFamily: 'Arial, sans-serif',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      padding: '2rem',
      backgroundColor: darkMode ? '#1a202c' : '#f7fafc',
      color: darkMode ? '#e2e8f0' : '#2d3748',
      transition: 'all 0.3s ease',
    },
    darkModeToggle: {
      position: 'fixed',
      top: '20px',
      right: '20px',
      background: darkMode ? '#ffd700' : '#2d3748',
      color: darkMode ? '#000' : '#fff',
      border: 'none',
      borderRadius: '50%',
      width: '50px',
      height: '50px',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      cursor: 'pointer',
      boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
      zIndex: 1000,
    },
    heroSection: {
      textAlign: 'center',
      maxWidth: '800px',
      marginBottom: '2rem',
    },
    heroTitle: {
      fontSize: '3rem',
      color: darkMode ? '#63b3ed' : '#3182ce',
      marginBottom: '1rem',
    },
    heroDescription: {
      color: darkMode ? '#a0aec0' : '#4a5568',
      fontSize: '1.1rem',
      lineHeight: '1.6',
    },
    featuresContainer: {
      display: 'flex',
      justifyContent: 'center',
      gap: '2rem',
      flexWrap: 'wrap',
      width: '100%',
      maxWidth: '1200px',
    },
    featureCard: {
      flex: '1',
      minWidth: '300px',
      maxWidth: '400px',
      padding: '1.5rem',
      borderRadius: '15px',
      backgroundColor: darkMode ? '#2d3748' : '#ffffff',
      boxShadow: darkMode 
        ? '0 4px 6px rgba(0,0,0,0.3)' 
        : '0 4px 6px rgba(0,0,0,0.1)',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
    },
    featureIcon: {
      fontSize: '3rem',
      marginBottom: '1rem',
    },
    featureTitle: {
      fontSize: '1.5rem',
      marginBottom: '0.5rem',
      fontWeight: 'bold',
      color: darkMode ? '#e2e8f0' : '#2d3748',
    },
    featureDescription: {
      color: darkMode ? '#a0aec0' : '#4a5568',
      marginBottom: '1rem',
    },
    exploreLink: {
      display: 'flex',
      alignItems: 'center',
      color: darkMode ? '#63b3ed' : '#3182ce',
    },
    ctaSection: {
      marginTop: '2rem',
      textAlign: 'center',
    },
    ctaText: {
      marginBottom: '1rem',
      color: darkMode ? '#a0aec0' : '#4a5568',
      fontSize: '1.2rem',
    },
    ctaButtonContainer: {
      display: 'flex',
      justifyContent: 'center',
      gap: '1rem',
    },
    ctaButton: {
      padding: '0.75rem 1.5rem',
      borderRadius: '9999px',
      display: 'flex',
      alignItems: 'center',
      gap: '0.5rem',
      border: 'none',
      cursor: 'pointer',
      backgroundColor: darkMode ? '#4299e1' : '#3182ce',
      color: '#ffffff',
      transition: 'all 0.3s ease',
    },
  };

  // Hover effect handlers
  const handleCardHoverIn = (e) => {
    e.currentTarget.style.transform = 'scale(1.05)';
  };

  const handleCardHoverOut = (e) => {
    e.currentTarget.style.transform = 'scale(1)';
  };

  return (
    <div style={styles.container}>
      {/* Dark Mode Toggle */}
      <button 
        onClick={toggleDarkMode}
        style={styles.darkModeToggle}
      >
        {darkMode ? <FaSun /> : <FaMoon />}
      </button>

      {/* Hero Section */}
      <div style={styles.heroSection}>
        <h1 style={styles.heroTitle}>
          Accessibility Companion
        </h1>
        <p style={styles.heroDescription}>
          Empowering communication through innovative technology. 
          Our app transforms barriers into bridges, making interaction 
          seamless and inclusive for everyone.
        </p>
      </div>

      {/* Features Section */}
      <div style={styles.featuresContainer}>
        {/* Chatbot Feature Card */}
        <div 
          style={styles.featureCard}
          onClick={() => navigate("/chatbot")}
          onMouseOver={handleCardHoverIn}
          onMouseOut={handleCardHoverOut}
        >
          <div style={{...styles.featureIcon, color: '#4299e1'}}>
            <FaRobot />
          </div>
          <h2 style={styles.featureTitle}>
            Interactive Chatbot
          </h2>
          <p style={styles.featureDescription}>
            AI-powered support system providing instant, personalized assistance.
          </p>
          <div style={styles.exploreLink}>
            <span>Explore</span>
            <FaArrowRight style={{ marginLeft: '0.5rem' }} />
          </div>
        </div>

        {/* Sign Language Feature Card */}
        <div 
          style={styles.featureCard}
          onClick={() => navigate("/sign-language")}
          onMouseOver={handleCardHoverIn}
          onMouseOut={handleCardHoverOut}
        >
          <div style={{...styles.featureIcon, color: '#48bb78'}}>
            <FaHandshake />
          </div>
          <h2 style={styles.featureTitle}>
            Sign Language Converter
          </h2>
          <p style={styles.featureDescription}>
            Bridge communication gaps with real-time sign language translation.
          </p>
          <div style={styles.exploreLink}>
            <span>Explore</span>
            <FaArrowRight style={{ marginLeft: '0.5rem' }} />
          </div>
        </div>

        {/* Text to Speech Feature Card */}
        <div 
          style={styles.featureCard}
          onClick={() => navigate("/text-to-speech")}
          onMouseOver={handleCardHoverIn}
          onMouseOut={handleCardHoverOut}
        >
          <div style={{...styles.featureIcon, color: '#f6ad55'}}>
            <FaVolumeUp />
          </div>
          <h2 style={styles.featureTitle}>
            Text to Speech
          </h2>
          <p style={styles.featureDescription}>
            Convert written text into clear and natural speech in real-time.
          </p>
          <div style={styles.exploreLink}>
            <span>Explore</span>
            <FaArrowRight style={{ marginLeft: '0.5rem' }} />
          </div>
        </div>

        {/* Text to Sign Feature Card */}
        <div 
          style={styles.featureCard}
          onClick={() => navigate("/text-to-sign")}
          onMouseOver={handleCardHoverIn}
          onMouseOut={handleCardHoverOut}
        >
          <div style={{...styles.featureIcon, color: '#9b2c2c'}}>
            <FaSignLanguage />
          </div>
          <h2 style={styles.featureTitle}>
            Text to Sign
          </h2>
          <p style={styles.featureDescription}>
            Transform text into visual sign language representations.
          </p>
          <div style={styles.exploreLink}>
            <span>Explore</span>
            <FaArrowRight style={{ marginLeft: '0.5rem' }} />
          </div>
        </div>

        {/* Healthbot Feature Card */}
        <div 
          style={styles.featureCard}
          onClick={() => navigate("/healthbot")}
          onMouseOver={handleCardHoverIn}
          onMouseOut={handleCardHoverOut}
        >
          <div style={{...styles.featureIcon, color: '#e53e3e'}}>
            <FaHeartbeat />
          </div>
          <h2 style={styles.featureTitle}>
            Healthbot
          </h2>
          <p style={styles.featureDescription}>
            A virtual assistant offering health advice and symptom checker.
          </p>
          <div style={styles.exploreLink}>
            <span>Explore</span>
            <FaArrowRight style={{ marginLeft: '0.5rem' }} />
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div style={styles.ctaSection}>
        <p style={styles.ctaText}>
          Ready to experience seamless communication?
        </p>
        <div style={styles.ctaButtonContainer}>
          <button 
            onClick={() => navigate("/chatbot")}
            style={styles.ctaButton}
            onMouseOver={(e) => e.currentTarget.style.opacity = '0.9'}
            onMouseOut={(e) => e.currentTarget.style.opacity = '1'}
          >
            <FaRobot /> Start Chatbot
          </button>
          <button 
            onClick={() => navigate("/sign-language")}
            style={{
              ...styles.ctaButton,
              backgroundColor: darkMode ? '#48bb78' : '#38b2ac',
            }}
            onMouseOver={(e) => e.currentTarget.style.opacity = '0.9'}
            onMouseOut={(e) => e.currentTarget.style.opacity = '1'}
          >
            <FaHandshake /> Sign Language
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
