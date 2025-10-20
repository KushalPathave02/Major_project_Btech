import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link, useLocation } from 'react-router-dom';

const VerifyEmail: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const [status, setStatus] = useState<'pending' | 'loading' | 'success' | 'error'>('pending');
  const [message, setMessage] = useState('');
  const [verifyLink, setVerifyLink] = useState<string | null>(null);

  const API_URL = process.env.REACT_APP_API_URL;

  // Get data from registration redirect
  const registrationData = location.state as { 
    email?: string; 
    name?: string; 
    verify_link?: string;
    message?: string;
  } | null;

  useEffect(() => {
    // If coming from registration, show verification pending state
    if (registrationData) {
      setStatus('pending');
      setVerifyLink(registrationData.verify_link || null);
      setMessage(registrationData.message || 'Please verify your email to continue.');
      return;
    }

    // If accessing verification link directly
    if (token) {
      verifyEmailWithToken();
    }
  }, [token, registrationData]);

  const verifyEmailWithToken = async () => {
    if (!token || !API_URL) {
      setStatus('error');
      setMessage('Invalid verification link or API URL not configured');
      return;
    }

    setStatus('loading');

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

  const handleVerifyClick = () => {
    if (verifyLink) {
      // Extract token from verify link and verify
      const tokenMatch = verifyLink.match(/\/verify\/([^?]+)/);
      if (tokenMatch) {
        const extractedToken = tokenMatch[1];
        navigate(`/verify/${extractedToken}`);
      } else {
        // Open link in new tab if token extraction fails
        window.open(verifyLink, '_blank');
      }
    }
  };

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
        maxWidth: '500px',
        width: '90%'
      }}>
        <div style={{ fontSize: '48px', marginBottom: '20px' }}>
          {status === 'pending' && '📧'}
          {status === 'loading' && '⏳'}
          {status === 'success' && '✅'}
          {status === 'error' && '❌'}
        </div>
        
        <h2 style={{ 
          color: '#333', 
          marginBottom: '20px',
          fontSize: '24px'
        }}>
          {status === 'pending' && 'Verify Your Email'}
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

        {status === 'pending' && verifyLink && (
          <div style={{ marginBottom: '30px' }}>
            <button
              onClick={handleVerifyClick}
              style={{
                background: 'linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)',
                color: 'white',
                padding: '15px 30px',
                borderRadius: '12px',
                border: 'none',
                fontSize: '16px',
                fontWeight: '600',
                cursor: 'pointer',
                marginBottom: '20px',
                transition: 'transform 0.2s',
                boxShadow: '0 4px 15px rgba(124, 58, 237, 0.3)'
              }}
              onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
              onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
            >
              Verify Email Now
            </button>
            
            <div style={{
              background: 'rgba(124, 58, 237, 0.1)',
              padding: '15px',
              borderRadius: '8px',
              marginTop: '15px'
            }}>
              <p style={{ fontSize: '14px', color: '#666', marginBottom: '10px' }}>
                Or copy this verification link:
              </p>
              <div style={{
                background: '#f8f9fa',
                padding: '10px',
                borderRadius: '6px',
                fontSize: '12px',
                wordBreak: 'break-all',
                color: '#495057',
                border: '1px solid #dee2e6'
              }}>
                {verifyLink}
              </div>
            </div>
          </div>
        )}

        {status === 'success' && (
          <div>
            <p style={{ color: '#28a745', fontSize: '14px', marginBottom: '20px' }}>
              Redirecting to login page in 3 seconds...
            </p>
            <Link 
              to="/login" 
              style={{
                display: 'inline-block',
                background: '#28a745',
                color: 'white',
                padding: '12px 24px',
                borderRadius: '8px',
                textDecoration: 'none',
                fontWeight: '600'
              }}
            >
              Go to Login Now
            </Link>
          </div>
        )}

        {status === 'error' && (
          <div>
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
                marginRight: '10px'
              }}
            >
              Go to Login
            </Link>
            <Link 
              to="/register" 
              style={{
                display: 'inline-block',
                background: '#6c757d',
                color: 'white',
                padding: '12px 24px',
                borderRadius: '8px',
                textDecoration: 'none',
                fontWeight: '600'
              }}
            >
              Register Again
            </Link>
          </div>
        )}

        {status === 'pending' && (
          <div style={{ marginTop: '30px', paddingTop: '20px', borderTop: '1px solid #eee' }}>
            <p style={{ fontSize: '14px', color: '#666', marginBottom: '10px' }}>
              Already verified?
            </p>
            <Link 
              to="/login" 
              style={{
                color: '#7c3aed',
                textDecoration: 'underline',
                fontWeight: '600'
              }}
            >
              Go to Login
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default VerifyEmail;
