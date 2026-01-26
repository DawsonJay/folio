import { useState, useEffect } from 'react';
import { useEvent } from '../hooks/useEventBus';
import { EVENT_TYPES } from '../events/eventTypes';

interface ChatBubbleProps {
  children: React.ReactNode;
}

export default function ChatBubble({ children }: ChatBubbleProps) {
  const initialText = typeof children === 'string' ? children : '';
  const [text, setText] = useState<string>(initialText);

  useEffect(() => {
    if (typeof children === 'string') {
      setText(children);
    }
  }, [children]);

  useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, (event) => {
    setText(event.answer);
  });

  return (
    <div className="chat-bubble">
      <div className="chat-bubble-content">
        {text}
      </div>
    </div>
  );
}

