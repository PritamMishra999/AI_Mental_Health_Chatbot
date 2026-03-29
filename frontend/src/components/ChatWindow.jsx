import { useEffect, useRef, useState } from 'react';
import { sendMessage } from '../services/api';
import RecommendationCard from './RecommendationCard';

function ChatWindow({ token, onLogout, userEmail }) {
  const [message, setMessage] = useState('');
  const [history, setHistory] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [history]);

  const handleSend = async (event) => {
    event.preventDefault();
    if (!message.trim()) {
      return;
    }

    const outgoing = { role: 'user', content: message };
    setHistory((prev) => [...prev, outgoing]);
    setMessage('');
    setLoading(true);

    try {
      const response = await sendMessage(message, token);
      setHistory((prev) => [...prev, { role: 'agent', content: response.response }]);
      setAnalysis({
        emotion: response.emotion,
        stressScore: response.stress_score,
        recommendation: response.recommendation,
      });
    } catch (err) {
      setHistory((prev) => [...prev, { role: 'agent', content: 'Sorry, I could not process that message right now.' }]);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="status-row">
        <span>Logged in as {userEmail || 'Chat user'}</span>
        <button className="secondary" onClick={onLogout}>Sign out</button>
      </div>

      <div className="card">
        <div ref={scrollRef} className="messages">
          {history.map((entry, index) => (
            <div key={index} className={`message ${entry.role}`}>
              <div className="bubble">{entry.content}</div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSend} style={{ marginTop: '18px' }}>
          <div className="form-group">
            <textarea
              rows="4"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              placeholder="Type how you are feeling or what is stressing you..."
            />
          </div>
          <button type="submit" disabled={loading}>{loading ? 'Sending…' : 'Send message'}</button>
        </form>
      </div>

      {analysis && <RecommendationCard analysis={analysis} />}
    </div>
  );
}

export default ChatWindow;
