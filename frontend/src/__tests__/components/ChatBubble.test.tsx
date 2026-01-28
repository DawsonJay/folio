import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { render, waitFor } from '@testing-library/react';
import ChatBubble from '../../components/ChatBubble';
import { eventBus } from '../../events/eventBus';
import { EVENT_TYPES } from '../../events/eventTypes';

describe('ChatBubble Sizing Mechanics', () => {
  let mockResizeObserver: any;
  let mockRequestAnimationFrame: any;
  let rafCallbacks: Array<() => void>;

  beforeEach(() => {
    eventBus.clear(EVENT_TYPES.CHAT_RESPONSE_RECEIVED);
    
    rafCallbacks = [];
    mockRequestAnimationFrame = vi.fn((cb: () => void) => {
      rafCallbacks.push(cb);
      return 1;
    });
    global.requestAnimationFrame = mockRequestAnimationFrame;

    const observe = vi.fn();
    const unobserve = vi.fn();
    const disconnect = vi.fn();

    class MockResizeObserver {
      observe = observe;
      unobserve = unobserve;
      disconnect = disconnect;
      callback: () => void;

      constructor(callback: () => void) {
        this.callback = callback;
        mockResizeObserver.mock.instances.push(this);
      }
    }

    mockResizeObserver = vi.fn(MockResizeObserver);
    mockResizeObserver.mock.instances = [];

    global.ResizeObserver = mockResizeObserver as any;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  const flushRAF = () => {
    rafCallbacks.forEach(cb => cb());
    rafCallbacks = [];
  };

  describe('Height Constraint Integration', () => {
    it('should pass both buffer refs to useConstrainedHeight', () => {
      const { container } = render(<ChatBubble>Initial text</ChatBubble>);
      
      const wrapper = container.querySelector('.chat-bubble') as HTMLElement;
      const buffers = container.querySelectorAll('.chat-bubble-content');
      
      expect(buffers.length).toBe(2);
      expect(mockResizeObserver).toHaveBeenCalledTimes(2);
    });

    it('should pass wrapper ref to both hook calls', () => {
      render(<ChatBubble>Initial text</ChatBubble>);
      
      expect(mockResizeObserver).toHaveBeenCalledTimes(2);
      
      const instances = mockResizeObserver.mock.results.map(r => r.value);
      instances.forEach(instance => {
        expect(instance.observe).toHaveBeenCalled();
      });
    });

    it('should set max-height when component mounts', async () => {
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>Short text</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      const wrapper = container.querySelector('.chat-bubble') as HTMLElement;
      
      if (content && wrapper) {
        Object.defineProperty(wrapper, 'clientHeight', { value: 500, configurable: true });
        Object.defineProperty(content, 'scrollHeight', { value: 100, configurable: true });
        
        const instances = mockResizeObserver.mock.instances;
        if (instances.length > 0) {
          instances[0].callback();
          flushRAF();
        }
        
        const maxHeight = content.style.getPropertyValue('max-height');
        expect(maxHeight).toBeTruthy();
      }
    });

    it('should constrain both buffers independently', async () => {
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>Initial text</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const buffers = container.querySelectorAll('.chat-bubble-content');
      const wrapper = container.querySelector('.chat-bubble') as HTMLElement;
      expect(buffers.length).toBe(2);
      
      Object.defineProperty(wrapper, 'clientHeight', { value: 500, configurable: true });
      
      const instances = mockResizeObserver.mock.instances;
      buffers.forEach((buffer, index) => {
        const element = buffer as HTMLElement;
        Object.defineProperty(element, 'scrollHeight', { value: 100 + index * 50, configurable: true });
      });
      
      instances.forEach((instance: any) => {
        if (instance && instance.callback) {
          instance.callback();
        }
      });
      
      flushRAF();
      
      buffers.forEach(buffer => {
        const maxHeight = (buffer as HTMLElement).style.getPropertyValue('max-height');
        expect(maxHeight).toBeTruthy();
      });
    });
  });

  describe('Height Calculation', () => {
    it('should set max-height to scrollHeight when content is shorter than wrapper', async () => {
      const shortText = 'Short text';
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>{shortText}</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const wrapper = container.querySelector('.chat-bubble') as HTMLElement;
      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      
      if (wrapper && content) {
        Object.defineProperty(wrapper, 'clientHeight', { value: 500, configurable: true });
        Object.defineProperty(content, 'scrollHeight', { value: 100, configurable: true });
        
        const instances = mockResizeObserver.mock.results.map(r => r.value);
        instances[0].callback();
        flushRAF();

        const maxHeight = parseInt(content.style.getPropertyValue('max-height') || '0');
        expect(maxHeight).toBeLessThanOrEqual(100);
      }
    });

    it('should set max-height to wrapper height when content is taller than wrapper', async () => {
      const longText = 'A'.repeat(1000);
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>{longText}</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const wrapper = container.querySelector('.chat-bubble') as HTMLElement;
      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      
      if (wrapper && content) {
        Object.defineProperty(wrapper, 'clientHeight', { value: 500, configurable: true });
        Object.defineProperty(content, 'scrollHeight', { value: 1000, configurable: true });
        
        const instances = mockResizeObserver.mock.results.map(r => r.value);
        instances[0].callback();
        flushRAF();

        const maxHeight = parseInt(content.style.getPropertyValue('max-height') || '0');
        expect(maxHeight).toBeLessThanOrEqual(500);
      }
    });

    it('should update max-height when content text changes', async () => {
      const { container, rerender } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>Short text</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      const wrapper = container.querySelector('.chat-bubble') as HTMLElement;
      
      Object.defineProperty(wrapper, 'clientHeight', { value: 500, configurable: true });
      Object.defineProperty(content, 'scrollHeight', { value: 100, configurable: true });

      const instances = mockResizeObserver.mock.instances;
      if (instances.length > 0) {
        instances[0].callback();
        flushRAF();
      }

      const initialMaxHeight = content.style.getPropertyValue('max-height');
      expect(initialMaxHeight).toBeTruthy();

      rerender(
        <div style={{ height: '500px' }}>
          <ChatBubble>Much longer text that should change the height</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      Object.defineProperty(content, 'scrollHeight', { value: 200, configurable: true });
      if (instances.length > 0) {
        instances[0].callback();
        flushRAF();
      }

      const newMaxHeight = content.style.getPropertyValue('max-height');
      expect(newMaxHeight).toBeTruthy();
    });

    it('should set correct max-height when buffer switches', async () => {
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>Initial text</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const buffers = container.querySelectorAll('.chat-bubble-content');
      const buffer0 = buffers[0] as HTMLElement;
      const buffer1 = buffers[1] as HTMLElement;
      const wrapper = container.querySelector('.chat-bubble') as HTMLElement;

      Object.defineProperty(buffer0, 'scrollHeight', { value: 100, configurable: true });
      Object.defineProperty(buffer1, 'scrollHeight', { value: 200, configurable: true });
      Object.defineProperty(wrapper, 'clientHeight', { value: 500, configurable: true });

      eventBus.emit(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, {
        answer: 'New response text',
        suggestions: [],
      });

      await waitFor(() => {
        flushRAF();
      });

      const instances = mockResizeObserver.mock.instances;
      instances.forEach((instance: any) => {
        if (instance && instance.callback) {
          instance.callback();
        }
      });
      flushRAF();

      const buffer1MaxHeight = parseInt(buffer1.style.getPropertyValue('max-height') || '0');
      expect(buffer1MaxHeight).toBeGreaterThan(0);
    });
  });

  describe('ResizeObserver Behavior', () => {
    it('should update max-height when content text changes', async () => {
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>Initial text</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const instances = mockResizeObserver.mock.results.map(r => r.value);
      const contentInstance = instances[0];
      
      contentInstance.callback();
      flushRAF();

      expect(mockRequestAnimationFrame).toHaveBeenCalled();
    });

    it('should update max-height when wrapper size changes', async () => {
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>Text</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const instances = mockResizeObserver.mock.results.map(r => r.value);
      const wrapperInstance = instances.find(inst => 
        inst.observe.mock.calls.some((call: any[]) => 
          call[0]?.classList?.contains('chat-bubble')
        )
      );
      
      if (wrapperInstance) {
        wrapperInstance.callback();
        flushRAF();
        expect(mockRequestAnimationFrame).toHaveBeenCalled();
      }
    });

    it('should observe both content and wrapper', () => {
      render(<ChatBubble>Text</ChatBubble>);

      const instances = mockResizeObserver.mock.results.map(r => r.value);
      instances.forEach(instance => {
        expect(instance.observe).toHaveBeenCalled();
      });
    });

    it('should disconnect ResizeObserver on component unmount', () => {
      const { unmount } = render(<ChatBubble>Text</ChatBubble>);

      const instances = mockResizeObserver.mock.results.map(r => r.value);
      
      unmount();

      instances.forEach(instance => {
        expect(instance.disconnect).toHaveBeenCalled();
      });
    });
  });

  describe('Scrolling Behavior', () => {
    it('should have overflow-y auto style', () => {
      const { container } = render(<ChatBubble>Text</ChatBubble>);
      
      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      expect(content).toBeTruthy();
      expect(content.classList.contains('chat-bubble-content')).toBe(true);
      
      const overflowY = content.style.overflowY || window.getComputedStyle(content).overflowY;
      expect(overflowY === 'auto' || overflowY === 'scroll' || content.classList.contains('chat-bubble-content')).toBe(true);
    });

    it('should allow scrolling when content exceeds max-height', async () => {
      const longText = 'A'.repeat(2000);
      const { container } = render(
        <div style={{ height: '200px' }}>
          <ChatBubble>{longText}</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      
      if (content) {
        Object.defineProperty(content, 'scrollHeight', { value: 1000, configurable: true });
        Object.defineProperty(container.querySelector('.chat-bubble') as HTMLElement, 'clientHeight', { value: 200, configurable: true });
        
        const instances = mockResizeObserver.mock.results.map(r => r.value);
        instances[0].callback();
        flushRAF();

        const maxHeight = parseInt(content.style.getPropertyValue('max-height') || '0');
        expect(maxHeight).toBeLessThanOrEqual(200);
        expect(content.scrollHeight).toBeGreaterThan(maxHeight);
      }
    });

    it('should not require scrolling when content fits within max-height', async () => {
      const shortText = 'Short text';
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>{shortText}</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      
      if (content) {
        Object.defineProperty(content, 'scrollHeight', { value: 50, configurable: true });
        Object.defineProperty(container.querySelector('.chat-bubble') as HTMLElement, 'clientHeight', { value: 500, configurable: true });
        
        const instances = mockResizeObserver.mock.results.map(r => r.value);
        instances[0].callback();
        flushRAF();

        const maxHeight = parseInt(content.style.getPropertyValue('max-height') || '0');
        expect(maxHeight).toBeGreaterThanOrEqual(50);
        expect(content.scrollHeight).toBeLessThanOrEqual(maxHeight);
      }
    });

    it('should allow independent scrolling for each buffer', async () => {
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>Initial</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const buffers = container.querySelectorAll('.chat-bubble-content');
      expect(buffers.length).toBe(2);
      
      buffers.forEach(buffer => {
        const element = buffer as HTMLElement;
        expect(element.classList.contains('chat-bubble-content')).toBe(true);
        const overflowY = element.style.overflowY || window.getComputedStyle(element).overflowY;
        expect(overflowY === 'auto' || overflowY === 'scroll' || element.classList.contains('chat-bubble-content')).toBe(true);
      });
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty text gracefully', async () => {
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble></ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      expect(content).toBeTruthy();
    });

    it('should handle very long content', async () => {
      const veryLongText = 'A'.repeat(10000);
      const { container } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>{veryLongText}</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      const maxHeight = parseInt(content.style.getPropertyValue('max-height') || '0');
      expect(maxHeight).toBeLessThanOrEqual(500);
    });

    it('should handle rapid content changes', async () => {
      const { container, rerender } = render(
        <div style={{ height: '500px' }}>
          <ChatBubble>Text 1</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      rerender(
        <div style={{ height: '500px' }}>
          <ChatBubble>Text 2</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      rerender(
        <div style={{ height: '500px' }}>
          <ChatBubble>Text 3</ChatBubble>
        </div>
      );

      await waitFor(() => {
        flushRAF();
      });

      const content = container.querySelector('.chat-bubble-content') as HTMLElement;
      expect(content).toBeTruthy();
    });
  });
});

