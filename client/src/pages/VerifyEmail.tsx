import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';

const VerifyEmail: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');

  const API_URL = process.env.REACT_APP_API_URL;

  useEffect(() => {
    const verifyEmail = async () => {
      if (!token || !API_URL) {
        setStatus('error');
        setMessage('Invalid verification link or API URL not configured');
        return;
      }

      try {
        const response = await fetch(`${API_URL}/api/auth/verify/${token}`);
        const data = await response.json();

        if (response.ok) {
          setStatus('success');
          setMessage(data.message || 'Email verified successfully!');
          // Redirect to login after 3 seconds
          setTimeout(() => {
            navigate('/login');
          }, 3000);
        } else {
          setStatus('error');
          setMessage(data.message || 'Verification failed');
        }
      } catch (error) {
        setStatus('error');
        setMessage('Network error occurred');
      }
    };

    verifyEmail();
  }, [token, API_URL, navigate]);

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <div style={{
        background: 'white',
        padding: '40px',
        borderRadius: '20px',
        boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
        textAlign: 'center',
        maxWidth: '400px',
        width: '90%'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '20px' }}>
          {status === 'loading' && '⏳'}
          {status === 'success' && '✅'}
          {status === 'error' && '❌'}
        </div>
        
        <h2 style={{ 
          color: '#333', 
          marginBottom: '20px',
          fontSize: '24px'
        }}>
          {status === 'loading' && 'Verifying Email...'}
          {status === 'success' && 'Email Verified!'}
          {status === 'error' && 'Verification Failed'}
        </h2>
        
        <p style={{ 
          color: '#666', 
          marginBottom: '30px',
          lineHeight: '1.5'
        }}>
          {message}
        </p>

        {status === 'success' && (
          <p style={{ color: '#28a745', fontSize: '14px' }}>
            Redirecting to login page in 3 seconds...
          </p>
        )}

        {status === 'error' && (
          <Link 
            to="/login" 
            style={{
              display: 'inline-block',
              background: '#7c3aed',
              color: 'white',
              padding: '12px 24px',
              borderRadius: '8px',
              textDecoration: 'none',
              fontWeight: '600',
              transition: 'background 0.3s'
            }}
          >
            Go to Login
          </Link>
        )}
      </div>
    </div>
  );
};

export default VerifyEmail;
