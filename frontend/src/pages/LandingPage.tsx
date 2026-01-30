import { useEffect, useRef } from 'react';
import Avatar from '../avatar/Avatar';
import Header from '../components/Header';
import InputBox from '../components/InputBox';
import Suggestions from '../components/Suggestions';
import ChatBubble from '../components/ChatBubble';
import './../styles/pages/_landing-page.scss';

export default function LandingPage() {
  const mainPanelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      mainPanelRef.current?.classList.add('loaded');
    }, 10);
    return () => clearTimeout(timer);
  }, []);


  return (
    <div className="landing-page">
      <Header />
      <div ref={mainPanelRef} className="main-panel">
        <div className="content">
          <div className="avatar-section">
            <Avatar />
            <ChatBubble>
              Hi! I'm Folio. I can answer questions about James's experience, skills, and projects. What would you like to know?
            </ChatBubble>
          </div>
          <div className="input-section">
            <InputBox />
            <Suggestions />
          </div>
        </div>
        <div className="content-spacer"></div>
      </div>
    </div>
  );
}
