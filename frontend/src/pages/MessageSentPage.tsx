import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import './../styles/pages/_get-in-touch-page.scss';

export default function MessageSentPage() {
  const mainPanelRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      mainPanelRef.current?.classList.add('loaded');
    }, 10);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="success-screen">
      <Header />
      <div ref={mainPanelRef} className="main-panel">
        <div className="content">
          <div className="success-message">
            <h1 className="success-title">Message Sent!</h1>
            <p className="success-text">
              Thanks for getting in touch, I'll get back to you within <span className="success-highlight">12 hours</span>.
            </p>
            <button 
              type="button" 
              onClick={() => navigate('/get-in-touch')}
              className="success-button"
            >
              Send Another Message
            </button>
          </div>
        </div>
        <div className="content-spacer"></div>
      </div>
    </div>
  );
}

