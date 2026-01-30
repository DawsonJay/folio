import { useState, useEffect, useRef } from 'react';
import { useEvent } from '../hooks/useEventBus';
import { useConstrainedHeight } from '../hooks/useConstrainedHeight';
import { EVENT_TYPES } from '../events/eventTypes';

interface ChatBubbleProps {
  children: React.ReactNode;
}

export default function ChatBubble({ children }: ChatBubbleProps) {
  const initialText = typeof children === 'string' ? children : '';
  const [activeBuffer, setActiveBuffer] = useState<number>(0);
  const [buffers, setBuffers] = useState<[string, string]>([initialText, '']);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const refs = [useRef<HTMLDivElement>(null), useRef<HTMLDivElement>(null)];

  const switchToBuffer = (text: string) => {
    const inactiveBuffer = activeBuffer === 0 ? 1 : 0;
    setBuffers(prev => {
      const newBuffers: [string, string] = [...prev];
      newBuffers[inactiveBuffer] = text;
      return newBuffers;
    });
    setActiveBuffer(inactiveBuffer);
  };

  const updateActiveBuffer = (text: string) => {
    setBuffers(prev => {
      const newBuffers: [string, string] = [...prev];
      newBuffers[activeBuffer] = text;
      return newBuffers;
    });
  };

  useEffect(() => {
    if (typeof children === 'string') {
      updateActiveBuffer(children);
    }
  }, [children]);

  useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, (event) => {
    switchToBuffer(event.answer);
  });

  useEvent(EVENT_TYPES.CHAT_ERROR, () => {
    switchToBuffer("Eerk! That didn't go as planned. I'm having trouble right now, try again in a moment?");
  });

  useConstrainedHeight(wrapperRef, refs[0]);
  useConstrainedHeight(wrapperRef, refs[1]);

  return (
    <div ref={wrapperRef} className="chat-bubble">
      {buffers.map((text, index) => (
        <div
          key={index}
          ref={refs[index]}
          className={`chat-bubble-content ${activeBuffer === index ? 'chat-bubble-content-active' : 'chat-bubble-content-inactive'}`}
        >
          {text}
        </div>
      ))}
    </div>
  );
}

