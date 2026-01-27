import { useState, useEffect, useRef } from 'react';
import { useEvent } from '../hooks/useEventBus';
import { useConstrainedHeight } from '../hooks/useConstrainedHeight';
import { EVENT_TYPES } from '../events/eventTypes';

interface ChatBubbleProps {
  children: React.ReactNode;
}

export default function ChatBubble({ children }: ChatBubbleProps) {
  const initialText = typeof children === 'string' ? children : '';
  const [text, setText] = useState<string>(initialText);
  const wrapperRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (typeof children === 'string') {
      setText(children);
    }
  }, [children]);

  useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, (event) => {
    setText(event.answer);
  });

  useConstrainedHeight(wrapperRef, contentRef);

  return (
    <div ref={wrapperRef} className="chat-bubble">
      <div ref={contentRef} className="chat-bubble-content">
        {text}
      </div>
    </div>
  );
}

