import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
const ChatbotPage = ({ darkMode = true }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const chatBoxRef = useRef(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Group messages by date
  const getMessageDate = () => {
    const today = new Date();
    return today.toLocaleDateString('en-US', { 
      weekday: 'long', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const sendMessage = async (e) => {
    e?.preventDefault();
    
    if (!input.trim()) return;

    const userMessage = { 
      text: input, 
      sender: "user",
      timestamp: new Date().toISOString() 
    };
    
    setMessages([...messages, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      // Add slight delay to simulate network request
      setTimeout(async () => {
        try {
          const response = await axios.post("http://localhost:5000/chat", { 
            message: input 
          });
  
          const botMessage = { 
            text: response.data.reply, 
            sender: "bot",
            timestamp: new Date().toISOString() 
          };
          
          setMessages((prev) => [...prev, botMessage]);
        } catch (error) {
          console.error("Error fetching response:", error);
          setMessages((prev) => [
            ...prev, 
            { 
              text: "Sorry, I couldn't process your request. Please try again later.", 
              sender: "bot",
              timestamp: new Date().toISOString()
            }
          ]);
        } finally {
          setIsTyping(false);
        }
      }, 1000);
    } catch (error) {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage(e);
    }
  };

  return (
    <div className="chat-container">
      <h1 className="chat-title">Gemini AI Assistant</h1>
      
      <div className="chat-box" ref={chatBoxRef}>
        {messages.length === 0 ? (
          <div className="empty-chat">
            <p>Send a message to start the conversation...</p>
          </div>
        ) : (
          <>
            <div className="date-divider">{getMessageDate()}</div>
            
            {messages.map((msg, index) => (
              <div 
                key={index} 
                className={`message ${msg.sender === "user" ? "user-message" : "bot-message"}`}
              >
                {msg.text}
              </div>
            ))}
          </>
        )}
        
        {isTyping && (
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <form className="input-container" onSubmit={sendMessage}>
        <input
          className="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          disabled={isTyping}
        />
        <button 
          className="send-button" 
          onClick={sendMessage}
          disabled={isTyping || !input.trim()}
          type="submit"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      </form>
      
      <div className="theme-toggle">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>
    </div>
  );
};

export default ChatbotPage;