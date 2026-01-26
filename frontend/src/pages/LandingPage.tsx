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
              Hi! I'm Folio. Ask me anything about James's skills, experience, or projects. This is a very long message to test the scrolling behavior of the chat bubble. I need to make this text long enough that it will definitely overflow the available space and trigger the scroll functionality. Let me add more text here to ensure we can see the scrolling in action. This paragraph should be long enough to demonstrate how the chat bubble handles content that exceeds its maximum height. The content should scroll smoothly within the bubble when it gets too long, allowing users to read all the information without the bubble expanding beyond the available space. This is important for maintaining a good user experience, especially on mobile devices where screen space is limited. The scrolling should work seamlessly and the bubble should maintain its design integrity while allowing users to access all the content. Now I'm adding even more text to make this message significantly longer. This additional content will help us test the scrolling functionality more thoroughly. We want to ensure that when the chat bubble receives a long response, it handles it gracefully by allowing users to scroll through the content. The design should remain clean and functional even with extensive text content. This is particularly important for a portfolio chatbot where responses might be detailed and comprehensive. Users should be able to read through all the information without feeling overwhelmed or losing track of where they are in the conversation. The scrolling mechanism needs to be intuitive and smooth, providing a pleasant reading experience. Let me continue adding more text to really push the limits of the scrolling functionality. This will help us identify any potential issues with the implementation and ensure that the chat bubble can handle various content lengths effectively. The goal is to create a robust component that works well regardless of how much text is contained within it. We want users to feel comfortable reading through long responses without the interface feeling cramped or difficult to navigate. The scrolling should feel natural and responsive, allowing users to easily access all the information they need. This is crucial for maintaining engagement and ensuring that users can fully benefit from the chatbot's responses. With more text, we can better test how the bubble adapts to different content scenarios and ensure it provides a consistent experience across various message lengths.
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
