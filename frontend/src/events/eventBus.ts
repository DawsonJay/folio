import type { ChatEvent, EventType } from './eventTypes';
import { logEvent } from '../utils/eventLogger';

type EventCallback<T extends ChatEvent> = (event: T) => void;

class EventBus {
  private static instance: EventBus;
  private listeners: Map<EventType, Set<EventCallback<ChatEvent>>> = new Map();

  private constructor() {}

  static getInstance(): EventBus {
    if (!EventBus.instance) {
      EventBus.instance = new EventBus();
    }
    return EventBus.instance;
  }

  on<T extends EventType>(
    eventType: T,
    callback: EventCallback<Extract<ChatEvent, { type: T }>>
  ): () => void {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, new Set());
    }

    const listeners = this.listeners.get(eventType)!;
    listeners.add(callback as EventCallback<ChatEvent>);

    return () => {
      listeners.delete(callback as EventCallback<ChatEvent>);
      if (listeners.size === 0) {
        this.listeners.delete(eventType);
      }
    };
  }

  emit<T extends EventType>(
    eventType: T,
    payload: Omit<Extract<ChatEvent, { type: T }>, 'type'>
  ): void {
    logEvent(eventType);
    const listeners = this.listeners.get(eventType);
    if (!listeners || listeners.size === 0) {
      return;
    }

    const event = { type: eventType, ...payload } as Extract<ChatEvent, { type: T }>;

    const listenersArray = Array.from(listeners);
    for (const callback of listenersArray) {
      try {
        callback(event);
      } catch (error) {
        console.error(`Error in event listener for ${eventType}:`, error);
      }
    }
  }

  off<T extends EventType>(
    eventType: T,
    callback: EventCallback<Extract<ChatEvent, { type: T }>>
  ): void {
    const listeners = this.listeners.get(eventType);
    if (listeners) {
      listeners.delete(callback as EventCallback<ChatEvent>);
      if (listeners.size === 0) {
        this.listeners.delete(eventType);
      }
    }
  }

  clear(eventType: EventType): void {
    this.listeners.delete(eventType);
  }

  listenerCount(eventType: EventType): number {
    return this.listeners.get(eventType)?.size ?? 0;
  }
}

export const eventBus = EventBus.getInstance();

