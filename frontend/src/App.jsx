import { useState } from 'react';
import AuthForm from './components/AuthForm';
import ChatWindow from './components/ChatWindow';

function App() {
  const [token, setToken] = useState(() => localStorage.getItem('chatbotToken'));
  const [userEmail, setUserEmail] = useState('');

  const handleLoginSuccess = (accessToken, email) => {
    localStorage.setItem('chatbotToken', accessToken);
    setToken(accessToken);
    setUserEmail(email);
  };

  const handleLogout = () => {
    localStorage.removeItem('chatbotToken');
    setToken(null);
    setUserEmail('');
  };

  return (
    <div className="app-shell">
      <header>
        <h1>Mental Health Support Chatbot</h1>
        <p>Real-time emotional support, stress insight, and wellness recommendations.</p>
      </header>

      {token ? (
        <ChatWindow token={token} onLogout={handleLogout} userEmail={userEmail} />
      ) : (
        <AuthForm onSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;
