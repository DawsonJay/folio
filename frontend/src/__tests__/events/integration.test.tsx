import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { useEvent, useEmit } from '../../hooks/useEventBus';
import { EVENT_TYPES } from '../../events/eventTypes';
import { eventBus } from '../../events/eventBus';
import type { AvatarEmotion } from '../../events/eventTypes';

describe('Event System Integration Tests', () => {
  beforeEach(() => {
    eventBus.clear(EVENT_TYPES.AVATAR_SET_EMOTION);
    eventBus.clear(EVENT_TYPES.CHAT_QUESTION_ASKED);
    eventBus.clear(EVENT_TYPES.CHAT_RESPONSE_RECEIVED);
    eventBus.clear(EVENT_TYPES.CHAT_ERROR);
    eventBus.clear(EVENT_TYPES.CHAT_READY);
  });

  describe('Avatar emotion flow', () => {
    it('should handle complete avatar emotion change flow', () => {
      const emotionHistory: AvatarEmotion[] = [];

      function AvatarComponent() {
        useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, (event) => {
          emotionHistory.push(event.emotion);
        });
        return <div data-testid="avatar">Avatar</div>;
      }

      function InputComponent() {
        const emit = useEmit();
        return (
          <button
            data-testid="ask-button"
            onClick={() => {
              emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'test' });
            }}
          >
            Ask
          </button>
        );
      }

      render(
        <>
          <AvatarComponent />
          <InputComponent />
        </>
      );

      const askButton = screen.getByTestId('ask-button');
      askButton.click();

      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'thinking' });
      eventBus.emit(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, { answer: 'Test answer' });
      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'surprised' });
      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

      expect(emotionHistory).toEqual(['thinking', 'surprised', 'happy']);
    });

    it('should handle error states correctly', () => {
      const emotionHistory: AvatarEmotion[] = [];

      function AvatarComponent() {
        useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, (event) => {
          emotionHistory.push(event.emotion);
        });
        useEvent(EVENT_TYPES.CHAT_ERROR, () => {
          eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'derp' });
        });
        return <div>Avatar</div>;
      }

      render(<AvatarComponent />);

      eventBus.emit(EVENT_TYPES.CHAT_ERROR, { error: 'Something went wrong' });

      expect(emotionHistory).toContain('derp');
    });

    it('should handle rate limiting state', () => {
      const emotionHistory: AvatarEmotion[] = [];

      function AvatarComponent() {
        useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, (event) => {
          emotionHistory.push(event.emotion);
        });
        return <div>Avatar</div>;
      }

      render(<AvatarComponent />);

      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'tired' });

      expect(emotionHistory).toContain('tired');
    });
  });

  describe('Chat flow', () => {
    it('should handle complete chat question and response flow', () => {
      const questions: string[] = [];
      const answers: string[] = [];

      function ChatComponent() {
        const emit = useEmit();

        useEvent(EVENT_TYPES.CHAT_QUESTION_ASKED, (event) => {
          questions.push(event.question);
        });

        useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, (event) => {
          answers.push(event.answer);
        });

        return (
          <button
            data-testid="submit"
            onClick={() => {
              emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'What is React?' });
            }}
          >
            Submit
          </button>
        );
      }

      render(<ChatComponent />);

      const submitButton = screen.getByTestId('submit');
      submitButton.click();

      expect(questions).toEqual(['What is React?']);

      eventBus.emit(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, {
        answer: 'React is a JavaScript library for building user interfaces.',
      });

      expect(answers).toEqual(['React is a JavaScript library for building user interfaces.']);
    });

    it('should handle multiple questions and responses', () => {
      const conversation: Array<{ question?: string; answer?: string }> = [];

      function ChatComponent() {
        const emit = useEmit();

        useEvent(EVENT_TYPES.CHAT_QUESTION_ASKED, (event) => {
          conversation.push({ question: event.question });
        });

        useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, (event) => {
          conversation.push({ answer: event.answer });
        });

        return (
          <div>
            <button
              data-testid="q1"
              onClick={() => emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'Q1' })}
            >
              Q1
            </button>
            <button
              data-testid="q2"
              onClick={() => emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'Q2' })}
            >
              Q2
            </button>
          </div>
        );
      }

      render(<ChatComponent />);

      screen.getByTestId('q1').click();
      eventBus.emit(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, { answer: 'A1' });

      screen.getByTestId('q2').click();
      eventBus.emit(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, { answer: 'A2' });

      expect(conversation).toEqual([
        { question: 'Q1' },
        { answer: 'A1' },
        { question: 'Q2' },
        { answer: 'A2' },
      ]);
    });
  });

  describe('Error propagation', () => {
    it('should propagate errors through the system', () => {
      const errors: string[] = [];
      const emotionHistory: AvatarEmotion[] = [];

      function ErrorHandlingComponent() {
        useEvent(EVENT_TYPES.CHAT_ERROR, (event) => {
          errors.push(event.error);
          eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'derp' });
        });

        useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, (event) => {
          emotionHistory.push(event.emotion);
        });

        return <div>Error Handler</div>;
      }

      render(<ErrorHandlingComponent />);

      eventBus.emit(EVENT_TYPES.CHAT_ERROR, { error: 'API Error' });

      expect(errors).toEqual(['API Error']);
      expect(emotionHistory).toContain('derp');
    });

    it('should handle error recovery flow', () => {
      const states: string[] = [];

      function RecoveryComponent() {
        useEvent(EVENT_TYPES.CHAT_ERROR, () => {
          states.push('error');
        });

        useEvent(EVENT_TYPES.CHAT_READY, () => {
          states.push('ready');
        });

        useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, () => {
          states.push('success');
        });

        return <div>Recovery</div>;
      }

      render(<RecoveryComponent />);

      eventBus.emit(EVENT_TYPES.CHAT_ERROR, { error: 'Error' });
      expect(states).toEqual(['error']);

      eventBus.emit(EVENT_TYPES.CHAT_READY, {});
      expect(states).toEqual(['error', 'ready']);

      eventBus.emit(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, { answer: 'Success' });
      expect(states).toEqual(['error', 'ready', 'success']);
    });
  });

  describe('Multiple components communication', () => {
    it('should allow multiple components to communicate via events', () => {
      const avatarEmotions: AvatarEmotion[] = [];
      const chatMessages: string[] = [];

      function AvatarComponent() {
        useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, (event) => {
          avatarEmotions.push(event.emotion);
        });
        return <div data-testid="avatar">Avatar</div>;
      }

      function ChatComponent() {
        useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, (event) => {
          chatMessages.push(event.answer);
        });
        return <div data-testid="chat">Chat</div>;
      }

      function InputComponent() {
        const emit = useEmit();
        return (
          <button
            data-testid="send"
            onClick={() => {
              emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'test' });
              emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'thinking' });
            }}
          >
            Send
          </button>
        );
      }

      render(
        <>
          <AvatarComponent />
          <ChatComponent />
          <InputComponent />
        </>
      );

      screen.getByTestId('send').click();

      expect(avatarEmotions).toEqual(['thinking']);

      eventBus.emit(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, { answer: 'Response' });
      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

      expect(chatMessages).toEqual(['Response']);
      expect(avatarEmotions).toEqual(['thinking', 'happy']);
    });
  });

  describe('Event order and timing', () => {
    it('should maintain event order', async () => {
      const eventOrder: string[] = [];

      function OrderTestComponent() {
        useEvent(EVENT_TYPES.CHAT_QUESTION_ASKED, () => {
          eventOrder.push('question');
        });

        useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, (event) => {
          if (event.emotion === 'thinking') {
            eventOrder.push('thinking');
          } else if (event.emotion === 'happy') {
            eventOrder.push('happy');
          }
        });

        useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, () => {
          eventOrder.push('response');
        });

        return <div>Order Test</div>;
      }

      render(<OrderTestComponent />);

      eventBus.emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'test' });
      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'thinking' });
      eventBus.emit(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, { answer: 'answer' });
      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

      expect(eventOrder).toEqual(['question', 'thinking', 'response', 'happy']);
    });
  });
});

