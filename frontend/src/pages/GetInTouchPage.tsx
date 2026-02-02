import { useEffect, useRef } from 'react';
import Header from '../components/Header';
import ContactForm from '../components/ContactForm';
import './../styles/pages/_get-in-touch-page.scss';

export default function GetInTouchPage() {
  const mainPanelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      mainPanelRef.current?.classList.add('loaded');
    }, 10);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="get-in-touch-page">
      <Header />
      <div ref={mainPanelRef} className="main-panel">
        <div className="content">
          <h1 className="page-title">Let's Talk Opportunities</h1>
          <p className="page-subtitle">Ready to start, no sponsorship required</p>

          <div className="contact-additional-info">
            <p className="contact-info-text">
              Working Holiday Visa approved means no sponsorship delays or costs. I can start with standard notice, relocate anywhere in Canada, and hit the ground running with your tech stack.
            </p>
          </div>

          <ContactForm />
        </div>
      </div>
    </div>
  );
}

