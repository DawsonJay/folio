import { describe, it, expect, beforeEach, vi } from 'vitest';
import { eventBus } from '../../events/eventBus';
import { EVENT_TYPES } from '../../events/eventTypes';
import type { ChatEvent } from '../../events/eventTypes';

describe('EventBus', () => {
  beforeEach(() => {
    eventBus.clear(EVENT_TYPES.AVATAR_SET_EMOTION);
    eventBus.clear(EVENT_TYPES.CHAT_QUESTION_ASKED);
    eventBus.clear(EVENT_TYPES.CHAT_RESPONSE_RECEIVED);
    eventBus.clear(EVENT_TYPES.CHAT_ERROR);
    eventBus.clear(EVENT_TYPES.CHAT_READY);
  });

  describe('Singleton instance', () => {
    it('should export a singleton instance', async () => {
      const { eventBus: eventBus2 } = await import('../../events/eventBus');
      expect(eventBus).toBe(eventBus2);
    });
  });

  describe('Listener registration (on)', () => {
    it('should register a listener and return unsubscribe function', () => {
      const callback = vi.fn();
      const unsubscribe = eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(1);
      expect(typeof unsubscribe).toBe('function');
    });

    it('should allow multiple listeners for the same event', () => {
      const callback1 = vi.fn();
      const callback2 = vi.fn();
      const callback3 = vi.fn();

      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback1);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback2);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback3);

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(3);
    });

    it('should not register the same callback twice', () => {
      const callback = vi.fn();
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(1);
    });
  });

  describe('Event emission (emit)', () => {
    it('should call all listeners when event is emitted', () => {
      const callback1 = vi.fn();
      const callback2 = vi.fn();
      const callback3 = vi.fn();

      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback1);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback2);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback3);

      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

      expect(callback1).toHaveBeenCalledTimes(1);
      expect(callback2).toHaveBeenCalledTimes(1);
      expect(callback3).toHaveBeenCalledTimes(1);
    });

    it('should pass correct event data to listeners', () => {
      const callback = vi.fn();
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'thinking' });

      expect(callback).toHaveBeenCalledWith({
        type: EVENT_TYPES.AVATAR_SET_EMOTION,
        emotion: 'thinking',
      });
    });

    it('should handle events with different payload structures', () => {
      const avatarCallback = vi.fn();
      const chatCallback = vi.fn();

      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, avatarCallback);
      eventBus.on(EVENT_TYPES.CHAT_QUESTION_ASKED, chatCallback);

      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });
      eventBus.emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'What is React?' });

      expect(avatarCallback).toHaveBeenCalledWith({
        type: EVENT_TYPES.AVATAR_SET_EMOTION,
        emotion: 'happy',
      });
      expect(chatCallback).toHaveBeenCalledWith({
        type: EVENT_TYPES.CHAT_QUESTION_ASKED,
        question: 'What is React?',
      });
    });

    it('should handle events with no payload', () => {
      const callback = vi.fn();
      eventBus.on(EVENT_TYPES.CHAT_READY, callback);

      eventBus.emit(EVENT_TYPES.CHAT_READY, {});

      expect(callback).toHaveBeenCalledWith({
        type: EVENT_TYPES.CHAT_READY,
      });
    });

    it('should not call listeners for different event types', () => {
      const callback = vi.fn();
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

      eventBus.emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'test' });

      expect(callback).not.toHaveBeenCalled();
    });

    it('should preserve listener order', () => {
      const callOrder: number[] = [];
      const callback1 = () => callOrder.push(1);
      const callback2 = () => callOrder.push(2);
      const callback3 = () => callOrder.push(3);

      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback1);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback2);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback3);

      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

      expect(callOrder).toEqual([1, 2, 3]);
    });
  });

  describe('Listener removal (off)', () => {
    it('should remove a specific listener', () => {
      const callback1 = vi.fn();
      const callback2 = vi.fn();

      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback1);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback2);

      eventBus.off(EVENT_TYPES.AVATAR_SET_EMOTION, callback1);

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(1);

      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

      expect(callback1).not.toHaveBeenCalled();
      expect(callback2).toHaveBeenCalledTimes(1);
    });

    it('should handle removing non-existent listener gracefully', () => {
      const callback = vi.fn();
      expect(() => {
        eventBus.off(EVENT_TYPES.AVATAR_SET_EMOTION, callback);
      }).not.toThrow();
    });
  });

  describe('Unsubscribe function', () => {
    it('should remove listener when unsubscribe is called', () => {
      const callback = vi.fn();
      const unsubscribe = eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(1);

      unsubscribe();

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(0);
    });

    it('should prevent listener from being called after unsubscribe', () => {
      const callback = vi.fn();
      const unsubscribe = eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

      unsubscribe();
      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

      expect(callback).not.toHaveBeenCalled();
    });

    it('should handle multiple unsubscribe calls gracefully', () => {
      const callback = vi.fn();
      const unsubscribe = eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

      unsubscribe();
      unsubscribe();

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(0);
    });
  });

  describe('Clear all listeners (clear)', () => {
    it('should remove all listeners for an event type', () => {
      const callback1 = vi.fn();
      const callback2 = vi.fn();
      const callback3 = vi.fn();

      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback1);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback2);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback3);

      eventBus.clear(EVENT_TYPES.AVATAR_SET_EMOTION);

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(0);

      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

      expect(callback1).not.toHaveBeenCalled();
      expect(callback2).not.toHaveBeenCalled();
      expect(callback3).not.toHaveBeenCalled();
    });
  });

  describe('Error handling', () => {
    it('should catch errors in listeners and continue calling other listeners', () => {
      const errorCallback = vi.fn(() => {
        throw new Error('Listener error');
      });
      const normalCallback = vi.fn();

      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, errorCallback);
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, normalCallback);

      expect(() => {
        eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });
      }).not.toThrow();

      expect(normalCallback).toHaveBeenCalledTimes(1);
    });

    it('should log errors to console', () => {
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      const errorCallback = vi.fn(() => {
        throw new Error('Test error');
      });

      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, errorCallback);
      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

      expect(consoleSpy).toHaveBeenCalledWith(
        expect.stringContaining('Error in event listener'),
        expect.any(Error)
      );

      consoleSpy.mockRestore();
    });
  });

  describe('Memory leak prevention', () => {
    it('should clean up listeners when unsubscribe is called', () => {
      const callback = vi.fn();
      const unsubscribe = eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(1);

      unsubscribe();

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(0);
    });

    it('should remove empty listener sets', () => {
      const callback = vi.fn();
      const unsubscribe = eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

      unsubscribe();

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(0);
    });
  });

  describe('Type safety', () => {
    it('should enforce correct payload types at compile time', () => {
      const callback = (event: Extract<ChatEvent, { type: typeof EVENT_TYPES.AVATAR_SET_EMOTION }>) => {
        expect(event.emotion).toBeDefined();
      };

      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);
      eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });
    });

    it('should prevent emitting wrong payload types', () => {
      const callback = vi.fn();
      eventBus.on(EVENT_TYPES.CHAT_QUESTION_ASKED, callback);

      eventBus.emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'test' });

      expect(callback).toHaveBeenCalledWith({
        type: EVENT_TYPES.CHAT_QUESTION_ASKED,
        question: 'test',
      });
    });
  });

  describe('Listener count', () => {
    it('should return 0 for event types with no listeners', () => {
      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(0);
    });

    it('should return correct count for event types with listeners', () => {
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, vi.fn());
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, vi.fn());
      eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, vi.fn());

      expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(3);
    });
  });
});

