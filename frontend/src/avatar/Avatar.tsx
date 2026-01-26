import { useState, useEffect, useRef } from 'react';
import { useEvent } from '../hooks/useEventBus';
import { EVENT_TYPES } from '../events/eventTypes';
import type { AvatarEmotion, AccentType } from '../events/eventTypes';
import faceHappy from '../assets/avatar/face-happy.png';
import faceThinking from '../assets/avatar/face-thinking.png';
import faceSurprised from '../assets/avatar/face-surprised.png';
import faceDerp from '../assets/avatar/face-derp.png';
import faceTired from '../assets/avatar/face-tired.png';
import faceAnnoyed from '../assets/avatar/face-annoyed.png';
import Accent from './Accent';

const HOLD_DELAY = 500;

type EmotionState = {
  emotion: AvatarEmotion;
  accent: AccentType;
};

const faceImages: Record<AvatarEmotion, string> = {
  happy: faceHappy,
  thinking: faceThinking,
  surprised: faceSurprised,
  derp: faceDerp,
  tired: faceTired,
  annoyed: faceAnnoyed,
};

export default function Avatar() {
  const [current, setCurrent] = useState<EmotionState>({
    emotion: 'happy',
    accent: null,
  });
  const [queue, setQueue] = useState<EmotionState[]>([]);
  const delayTimeoutRef = useRef<number | null>(null);

  const delay = (callback: () => void) => {
    if (delayTimeoutRef.current !== null) return;

    const timeout = setTimeout(() => {
      delayTimeoutRef.current = null;
      callback();
    }, HOLD_DELAY);

    delayTimeoutRef.current = timeout;
  };

  const updateFromQueue = () => {
    setQueue((prevQueue) => {
      if (prevQueue.length === 0) return prevQueue;

      const nextItem = prevQueue[0];
      setCurrent(nextItem);

      delay(() => {
        updateFromQueue();
      });

      return prevQueue.slice(1);
    });
  };

  useEffect(() => {
    if (queue.length > 0 && delayTimeoutRef.current === null) {
      updateFromQueue();
    }
  }, [queue]);

  useEffect(() => {
    return () => {
      if (delayTimeoutRef.current) {
        clearTimeout(delayTimeoutRef.current);
      }
    };
  }, []);

  const addToQueue = (emotions: EmotionState[]) => {
    setQueue((prevQueue) => {
      if (emotions.length === 0) return prevQueue;

      const compareItem =
        prevQueue.length > 0
          ? prevQueue[prevQueue.length - 1]
          : current;

      const firstNewItem = emotions[0];
      const shouldSkipFirst =
        compareItem.emotion === firstNewItem.emotion &&
        compareItem.accent === firstNewItem.accent;

      const emotionsToAdd = shouldSkipFirst ? emotions.slice(1) : emotions;

      return [...prevQueue, ...emotionsToAdd];
    });
  };

  const responseSuccess = () => {
    addToQueue([
      { emotion: 'surprised', accent: 'sparkles' },
      { emotion: 'happy', accent: null },
    ]);
  };

  const responseError = () => {
    addToQueue([
      { emotion: 'surprised', accent: 'sparkles' },
      { emotion: 'derp', accent: null },
    ]);
  };

  const responseQuestion = () => {
    addToQueue([{ emotion: 'thinking', accent: 'questionMarks' }]);
  };

  useEvent(EVENT_TYPES.CHAT_QUESTION_ASKED, () => {
    responseQuestion();
  });

  useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, () => {
    responseSuccess();
  });

  useEvent(EVENT_TYPES.CHAT_ERROR, () => {
    responseError();
  });

  return (
    <div className="avatar">
      <div className="avatar-container">
        <img src={faceImages[current.emotion]} alt={`Avatar ${current.emotion}`} />
        <Accent accent={current.accent} />
      </div>
    </div>
  );
}

