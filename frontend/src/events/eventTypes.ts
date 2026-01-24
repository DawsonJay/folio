export const EVENT_TYPES = {
  AVATAR_SET_EMOTION: 'avatar:setEmotion',
  CHAT_QUESTION_ASKED: 'chat:questionAsked',
  CHAT_RESPONSE_RECEIVED: 'chat:responseReceived',
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
  | { type: typeof EVENT_TYPES.AVATAR_SET_EMOTION; emotion: AvatarEmotion }
  | { type: typeof EVENT_TYPES.CHAT_QUESTION_ASKED; question: string }
  | { type: typeof EVENT_TYPES.CHAT_RESPONSE_RECEIVED; answer: string }
  | { type: typeof EVENT_TYPES.CHAT_ERROR; error: string }
  | { type: typeof EVENT_TYPES.CHAT_READY };

