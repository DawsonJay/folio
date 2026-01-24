import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, waitFor } from '@testing-library/react';
import { useEffect } from 'react';
import { useEvent, useEmit } from '../../hooks/useEventBus';
import { EVENT_TYPES } from '../../events/eventTypes';
import { eventBus } from '../../events/eventBus';

describe('useEvent', () => {
  beforeEach(() => {
    eventBus.clear(EVENT_TYPES.AVATAR_SET_EMOTION);
    eventBus.clear(EVENT_TYPES.CHAT_QUESTION_ASKED);
    eventBus.clear(EVENT_TYPES.CHAT_RESPONSE_RECEIVED);
    eventBus.clear(EVENT_TYPES.CHAT_ERROR);
    eventBus.clear(EVENT_TYPES.CHAT_READY);
  });

  it('should subscribe to events correctly', () => {
    const callback = vi.fn();
    
    function TestComponent() {
      useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, callback);
      return <div>Test</div>;
    }

    render(<TestComponent />);
    
    eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

    expect(callback).toHaveBeenCalledWith({
      type: EVENT_TYPES.AVATAR_SET_EMOTION,
      emotion: 'happy',
    });
  });

  it('should automatically clean up on unmount', () => {
    const callback = vi.fn();

    function TestComponent() {
      useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, callback);
      return <div>Test</div>;
    }

    const { unmount } = render(<TestComponent />);
    
    expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(1);

    unmount();

    expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(0);

    eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });
    expect(callback).not.toHaveBeenCalled();
  });

  it('should handle multiple useEvent calls in same component', () => {
    const callback1 = vi.fn();
    const callback2 = vi.fn();
    const callback3 = vi.fn();

    function TestComponent() {
      useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, callback1);
      useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, callback2);
      useEvent(EVENT_TYPES.CHAT_QUESTION_ASKED, callback3);
      return <div>Test</div>;
    }

    render(<TestComponent />);

    eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });
    eventBus.emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'test' });

    expect(callback1).toHaveBeenCalledTimes(1);
    expect(callback2).toHaveBeenCalledTimes(1);
    expect(callback3).toHaveBeenCalledTimes(1);
  });

  it('should clean up all listeners on unmount', () => {
    const callback1 = vi.fn();
    const callback2 = vi.fn();

    function TestComponent() {
      useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, callback1);
      useEvent(EVENT_TYPES.CHAT_QUESTION_ASKED, callback2);
      return <div>Test</div>;
    }

    const { unmount } = render(<TestComponent />);

    expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(1);
    expect(eventBus.listenerCount(EVENT_TYPES.CHAT_QUESTION_ASKED)).toBe(1);

    unmount();

    expect(eventBus.listenerCount(EVENT_TYPES.AVATAR_SET_EMOTION)).toBe(0);
    expect(eventBus.listenerCount(EVENT_TYPES.CHAT_QUESTION_ASKED)).toBe(0);
  });

  it('should update when callback changes', () => {
    const callback1 = vi.fn();
    const callback2 = vi.fn();

    function TestComponent({ useCallback1 }: { useCallback1: boolean }) {
      useEvent(
        EVENT_TYPES.AVATAR_SET_EMOTION,
        useCallback1 ? callback1 : callback2
      );
      return <div>Test</div>;
    }

    const { rerender } = render(<TestComponent useCallback1={true} />);

    eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });
    expect(callback1).toHaveBeenCalledTimes(1);
    expect(callback2).not.toHaveBeenCalled();

    rerender(<TestComponent useCallback1={false} />);

    eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'thinking' });
    expect(callback1).toHaveBeenCalledTimes(1);
    expect(callback2).toHaveBeenCalledTimes(1);
  });

  it('should work with multiple components', () => {
    const callback1 = vi.fn();
    const callback2 = vi.fn();

    function Component1() {
      useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, callback1);
      return <div>Component1</div>;
    }

    function Component2() {
      useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, callback2);
      return <div>Component2</div>;
    }

    render(
      <>
        <Component1 />
        <Component2 />
      </>
    );

    eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

    expect(callback1).toHaveBeenCalledTimes(1);
    expect(callback2).toHaveBeenCalledTimes(1);
  });

  it('should handle type-safe event callbacks', () => {
    const callback = vi.fn((event) => {
      expect(event.emotion).toBeDefined();
    });

    function TestComponent() {
      useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, callback);
      return <div>Test</div>;
    }

    render(<TestComponent />);
    eventBus.emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

    expect(callback).toHaveBeenCalled();
  });
});

describe('useEmit', () => {
  it('should return an emit function', () => {
    let emitFn: ReturnType<typeof useEmit> | null = null;

    function TestComponent() {
      emitFn = useEmit();
      return <div>Test</div>;
    }

    render(<TestComponent />);

    expect(emitFn).toBeDefined();
    expect(typeof emitFn).toBe('function');
  });

  it('should emit events correctly', () => {
    const callback = vi.fn();
    eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

    let emitFn: ReturnType<typeof useEmit> | null = null;

    function TestComponent() {
      emitFn = useEmit();
      return <div>Test</div>;
    }

    render(<TestComponent />);

    emitFn!(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });

    expect(callback).toHaveBeenCalledWith({
      type: EVENT_TYPES.AVATAR_SET_EMOTION,
      emotion: 'happy',
    });
  });

  it('should be type-safe', () => {
    const callback = vi.fn();
    eventBus.on(EVENT_TYPES.CHAT_QUESTION_ASKED, callback);

    let emitFn: ReturnType<typeof useEmit> | null = null;

    function TestComponent() {
      emitFn = useEmit();
      return <div>Test</div>;
    }

    render(<TestComponent />);

    emitFn!(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'What is React?' });

    expect(callback).toHaveBeenCalledWith({
      type: EVENT_TYPES.CHAT_QUESTION_ASKED,
      question: 'What is React?',
    });
  });

  it('should handle events with no payload', () => {
    const callback = vi.fn();
    eventBus.on(EVENT_TYPES.CHAT_READY, callback);

    let emitFn: ReturnType<typeof useEmit> | null = null;

    function TestComponent() {
      emitFn = useEmit();
      return <div>Test</div>;
    }

    render(<TestComponent />);

    emitFn!(EVENT_TYPES.CHAT_READY, {});

    expect(callback).toHaveBeenCalledWith({
      type: EVENT_TYPES.CHAT_READY,
    });
  });

  it('should return the same emit function on re-render', () => {
    let emitFn1: ReturnType<typeof useEmit> | null = null;
    let emitFn2: ReturnType<typeof useEmit> | null = null;

    function TestComponent() {
      const emit = useEmit();
      if (!emitFn1) {
        emitFn1 = emit;
      } else {
        emitFn2 = emit;
      }
      return <div>Test</div>;
    }

    const { rerender } = render(<TestComponent />);
    rerender(<TestComponent />);

    expect(emitFn1).toBe(emitFn2);
  });

  it('should work with multiple components', () => {
    const callback = vi.fn();
    eventBus.on(EVENT_TYPES.AVATAR_SET_EMOTION, callback);

    let emitFn1: ReturnType<typeof useEmit> | null = null;
    let emitFn2: ReturnType<typeof useEmit> | null = null;

    function Component1() {
      emitFn1 = useEmit();
      return <div>Component1</div>;
    }

    function Component2() {
      emitFn2 = useEmit();
      return <div>Component2</div>;
    }

    render(
      <>
        <Component1 />
        <Component2 />
      </>
    );

    emitFn1!(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });
    emitFn2!(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'thinking' });

    expect(callback).toHaveBeenCalledTimes(2);
  });
});

describe('useEvent and useEmit integration', () => {
  it('should work together in the same component', async () => {
    const receivedEvents: any[] = [];

    function TestComponent() {
      useEvent(EVENT_TYPES.AVATAR_SET_EMOTION, (event) => {
        receivedEvents.push(event);
      });
      const emit = useEmit();

      useEffect(() => {
        emit(EVENT_TYPES.AVATAR_SET_EMOTION, { emotion: 'happy' });
      }, [emit]);

      return <div>Test</div>;
    }

    render(<TestComponent />);

    await waitFor(() => {
      expect(receivedEvents).toHaveLength(1);
    });

    expect(receivedEvents[0]).toEqual({
      type: EVENT_TYPES.AVATAR_SET_EMOTION,
      emotion: 'happy',
    });
  });
});

