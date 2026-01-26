import type { Suggestion } from '../types';

export const EVENT_TYPES = {
  CHAT_QUESTION_ASKED: 'chat:questionAsked',
  CHAT_RESPONSE_RECEIVED: 'chat:responseReceived',
  INITIAL_SUGGESTIONS_RECEIVED: 'chat:initialSuggestionsReceived',
  CHAT_ERROR: 'chat:error',
  CHAT_READY: 'chat:ready',
} as const;

export type EventType = typeof EVENT_TYPES[keyof typeof EVENT_TYPES];

export type AvatarEmotion =
  | 'happy'
  | 'thinking'
  | 'surprised'
  | 'derp'
  | 'tired'
  | 'annoyed';

export type AccentType =
  | 'questionMarks'
  | 'sparkles'
  | 'zzz'
  | 'huff'
  | null;

export type ChatEvent =
  | { type: typeof EVENT_TYPES.CHAT_QUESTION_ASKED; question: string }
  | { type: typeof EVENT_TYPES.CHAT_RESPONSE_RECEIVED; answer: string; suggestions: Suggestion[] }
  | { type: typeof EVENT_TYPES.INITIAL_SUGGESTIONS_RECEIVED; suggestions: Suggestion[] }
  | { type: typeof EVENT_TYPES.CHAT_ERROR; error: string }
  | { type: typeof EVENT_TYPES.CHAT_READY };

