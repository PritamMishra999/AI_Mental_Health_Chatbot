import { useState } from 'react';
import { login, register } from '../services/api';

function AuthForm({ onSuccess }) {
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (mode === 'login') {
        const result = await login(email, password);
        onSuccess(result.access_token, email);
      } else {
        await register(email, password, fullName);
        const result = await login(email, password);
        onSuccess(result.access_token, email);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>{mode === 'login' ? 'Welcome back' : 'Create your account'}</h2>
      <p>{mode === 'login' ? 'Sign in to continue your wellness journey.' : 'Register to save your conversation history.'}</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email</label>
          <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
        </div>

        {mode === 'register' && (
          <div className="form-group">
            <label>Full name</label>
            <input value={fullName} onChange={(event) => setFullName(event.target.value)} required />
          </div>
        )}

        <div className="form-group">
          <label>Password</label>
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
        </div>

        {error && <p style={{ color: '#b91c1c' }}>{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? 'Working…' : mode === 'login' ? 'Sign in' : 'Register'}
        </button>
      </form>

      <div style={{ marginTop: '16px' }}>
        <button type="button" className="secondary" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}> 
          {mode === 'login' ? 'Create an account' : 'Already have an account? Sign in'}
        </button>
      </div>
    </div>
  );
}

export default AuthForm;
