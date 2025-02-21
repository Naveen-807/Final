import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, NavLink } from "react-router-dom";

// Import your page components
import Home from "./pages/Home";
import ChatbotPage from "./pages/ChatbotPage";
import SignLanguagePage from "./pages/SignlanguagePage";

import "./App.css";

// NotFound Component
const NotFound = () => {
  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-red-500">404</h1>
        <p className="text-xl mt-4">Page Not Found</p>
        <NavLink 
          to="/" 
          className="mt-6 inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Return Home
        </NavLink>
      </div>
    </div>
  );
};

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  // Navigation link styles
  const navLinkStyle = ({ isActive }) => 
    `${isActive ? 'bg-blue-700 text-white' : 'text-white'} 
    hover:bg-blue-600 px-3 py-2 rounded-md transition duration-300`;

  return (
    <Router>
      <div className="min-h-screen bg-gray-100 text-gray-800">
        {/* Navigation Bar */}
        <nav className="bg-blue-500 p-4">
          <div className="container mx-auto flex justify-between items-center">
            {/* Logo or App Name */}
            <div className="text-white text-xl font-bold">
              MyApp
            </div>

            {/* Mobile Menu Toggle */}
            <div className="md:hidden">
              <button 
                onClick={toggleMenu} 
                className="text-white focus:outline-none"
              >
                {isMenuOpen ? 'Close' : 'Menu'}
              </button>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden md:flex space-x-4">
              <NavLink to="/" className={navLinkStyle}>
                Home
              </NavLink>
              <NavLink to="/chatbot" className={navLinkStyle}>
                Chatbot
              </NavLink>
              <NavLink to="/sign-language" className={navLinkStyle}>
                Sign Language
              </NavLink>
            </div>
          </div>

          {/* Mobile Menu */}
          {isMenuOpen && (
            <div className="md:hidden">
              <div className="px-2 pt-2 pb-3 space-y-1">
                <NavLink 
                  to="/" 
                  className="block text-white hover:bg-blue-600 px-3 py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Home
                </NavLink>
                <NavLink 
                  to="/chatbot" 
                  className="block text-white hover:bg-blue-600 px-3 py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Chatbot
                </NavLink>
                <NavLink 
                  to="/sign-language" 
                  className="block text-white hover:bg-blue-600 px-3 py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Sign Language
                </NavLink>
                
              </div>
            </div>
          )}
        </nav>

        {/* Page Content */}
        <div className="container mx-auto mt-4">
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