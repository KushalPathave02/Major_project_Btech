import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';


const Register: React.FC = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [verifyLink, setVerifyLink] = useState<string | null>(null);
  const navigate = useNavigate();

  const API_URL = process.env.REACT_APP_API_URL;
const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);
    if (!API_URL) {
      setError('API URL not set. Please configure REACT_APP_API_URL in your .env file.');
      setLoading(false);
      return;
    }
    try {
      const res = await fetch(`${API_URL}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess(true);
        // Redirect to verification page with registration data
        setTimeout(() => {
          navigate('/verify-email', {
            state: {
              email: email,
              name: name,
              verify_link: data.verify_link,
              message: data.message
            }
          });
        }, 1500);
      } else {
        setError(data.message || 'Registration failed');
      }
    } catch (err) {
      setError('Network error');
    }
    setLoading(false);
  };

  return (
    <div style={{ position: 'relative', minHeight: '100vh', width: '100vw', overflow: 'hidden' }}>

      {/* Register Form Overlay */}
      <div style={{ position: 'relative', zIndex: 2, maxWidth: 320, width: '100%', background: 'linear-gradient(120deg, #23263a 0%, #7c3aed 100%)', borderRadius: 20, padding: 40, boxShadow: '0 6px 32px rgba(44,62,80,0.18)', color: '#fff', display: 'flex', flexDirection: 'column', alignItems: 'center', margin: '0 auto', top: '50%', transform: 'translateY(25vh)' }}>
        <div style={{ fontWeight: 800, fontSize: 26, letterSpacing: 1, marginBottom: 24, color: '#7c3aed' }}>FinTrack+</div>
        <h2 style={{ textAlign: 'center', marginBottom: 24, fontWeight: 700 }}>Register</h2>
        <form onSubmit={handleSubmit} style={{ width: '100%' }}>
          <label style={{ marginBottom: 8, fontSize: 16, fontWeight: 500, color: '#fff' }}>Name:</label>
          <input
            type="text"
            value={name}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setName(e.target.value)}
            required
            style={{ width: '100%', marginBottom: 16, padding: '16px 8px', fontSize: 16, fontWeight: 500, color: '#fff', background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: 8, height: '28px', boxSizing: 'border-box' }}
          />
          <label style={{ marginBottom: 8, fontSize: 16, fontWeight: 500, color: '#fff' }}>Email:</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            style={{ width: '100%', marginBottom: 16, padding: '16px 8px', fontSize: 16, fontWeight: 500, color: '#fff', background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: 8, height: '28px', boxSizing: 'border-box' }}
          />
          <label style={{ marginBottom: 8, fontSize: 16, fontWeight: 500, color: '#fff' }}>Password:</label>
          <div style={{ position: 'relative', marginBottom: 16, display: 'flex', alignItems: 'center' }}>
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              style={{ 
                width: '100%', 
                padding: '16px 45px 16px 8px', 
                fontSize: 16, 
                fontWeight: 500, 
                color: '#fff', 
                background: 'rgba(255,255,255,0.1)', 
                border: 'none', 
                borderRadius: 8,
                height: '28px',
                boxSizing: 'border-box'
              }}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              style={{
                position: 'absolute',
                right: '6px',
                top: '50%',
                transform: 'translateY(-50%)',
                background: 'none',
                border: 'none',
                color: '#b0b8d1',
                cursor: 'pointer',
                padding: '6px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '32px',
                height: '32px',
                borderRadius: '4px'
              }}
            >
              {showPassword ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/>
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z"/>
                </svg>
              )}
            </button>
          </div>
          <button type="submit" disabled={loading} style={{ width: '100%', padding: 10, fontSize: 16, fontWeight: 700, color: '#fff', background: 'linear-gradient(120deg, #7c3aed 0%, #7c3aed 100%)', border: 'none', borderRadius: 8, cursor: 'pointer' }}>
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>
        {error && <div style={{ color: 'red', marginTop: 16, fontSize: 16, fontWeight: 500 }}>{error}</div>}
        {success && (
          <div style={{ color: 'green', marginTop: 16, fontSize: 16, fontWeight: 500 }}>
            <p>Registration successful! Redirecting to verification page...</p>
          </div>
        )}
        <div style={{ marginTop: 24, textAlign: 'center' }}>
          <span style={{ color: '#b0b8d1', fontSize: 15 }}>Already have an account?</span>
          <br />
          <Link to="/login" style={{ color: '#fdfcfdff', fontWeight: 700, textDecoration: 'underline', fontSize: 16, cursor: 'pointer' }}>
            Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Register;
