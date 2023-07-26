import React from 'react';
import './Chatbot.css';

const Chatbot = () => {
  return (
    <div className="chatbot-container">
      <div className="chatbot-messages">
        <div className="user-message">Hello, how can I help you?</div>
        <div className="bot-message">Hi! I'm a chatbot.</div>
      </div>
      <div className="chatbot-input">
        <input type="text" placeholder="Paste code..." />
        <button>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
