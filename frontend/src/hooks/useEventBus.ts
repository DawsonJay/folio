import { useEffect, useCallback } from 'react';
import { eventBus } from '../events/eventBus';
import type { ChatEvent, EventType } from '../events/eventTypes';

export function useEvent<T extends EventType>(
  eventType: T,
  callback: (event: Extract<ChatEvent, { type: T }>) => void
): void {
  useEffect(() => {
    const unsubscribe = eventBus.on(eventType, callback);
    return unsubscribe;
  }, [eventType, callback]);
}

export function useEmit(): <T extends EventType>(
  eventType: T,
  payload: Omit<Extract<ChatEvent, { type: T }>, 'type'>
) => void {
  return useCallback(<T extends EventType>(
    eventType: T,
    payload: Omit<Extract<ChatEvent, { type: T }>, 'type'>
  ) => {
    eventBus.emit(eventType, payload);
  }, []);
}

