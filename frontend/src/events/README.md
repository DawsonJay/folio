# Event System

Type-safe, centralized event system for component communication in the Folio frontend.

## Overview

The event system enables decoupled component communication through a singleton event bus. Components can emit and listen to events without direct dependencies, making the codebase more modular and testable.

## Key Features

- **Type-safe**: Discriminated unions ensure compile-time type safety
- **Centralized**: All event types defined in one place (`eventTypes.ts`)
- **Automatic cleanup**: React hooks handle listener cleanup automatically
- **Error handling**: Errors in listeners don't stop other listeners
- **Memory safe**: Proper cleanup prevents memory leaks

## Usage

### Basic Event Emission

```tsx
import { useEmit } from '../hooks/useEventBus';
import { EVENT_TYPES } from '../events/eventTypes';

function InputComponent() {
  const emit = useEmit();
  
  const handleSubmit = (question: string) => {
    emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question });
  };
  
  return <input onSubmit={handleSubmit} />;
}
```

### Basic Event Listening

```tsx
import { useEvent } from '../hooks/useEventBus';
import { EVENT_TYPES } from '../events/eventTypes';

function ChatComponent() {
  const [answer, setAnswer] = useState('');
  
  useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, (event) => {
    setAnswer(event.answer);
  });
  
  return <div>{answer}</div>;
}
```

### Multiple Listeners

```tsx
function ChatComponent() {
  useEvent(EVENT_TYPES.CHAT_QUESTION_ASKED, (event) => {
    console.log('Question:', event.question);
  });
  
  useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, (event) => {
    console.log('Answer:', event.answer);
  });
  
  useEvent(EVENT_TYPES.CHAT_ERROR, (event) => {
    console.error('Error:', event.error);
  });
  
  return <div>Chat</div>;
}
```

### Direct EventBus Usage (Outside React)

```tsx
import { eventBus } from '../events/eventBus';
import { EVENT_TYPES } from '../events/eventTypes';

// Subscribe
const unsubscribe = eventBus.on(EVENT_TYPES.CHAT_QUESTION_ASKED, (event) => {
  console.log(event.question);
});

// Emit
eventBus.emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: 'test' });

// Unsubscribe
unsubscribe();
```

## Event Types

All event types are defined in `eventTypes.ts`:

- `EVENT_TYPES.CHAT_QUESTION_ASKED` - User submitted a question
- `EVENT_TYPES.CHAT_RESPONSE_RECEIVED` - AI response received
- `EVENT_TYPES.INITIAL_SUGGESTIONS_RECEIVED` - Initial suggestions received
- `EVENT_TYPES.CHAT_ERROR` - Error occurred
- `EVENT_TYPES.CHAT_READY` - Chat system ready

See `eventTypes.ts` for complete type definitions and payload structures.

## Best Practices

1. **Always use `EVENT_TYPES` constants** - Never use string literals directly
2. **Use React hooks in components** - `useEvent` and `useEmit` handle cleanup automatically
3. **Keep callbacks stable** - Use `useCallback` if callback depends on props/state
4. **One listener per concern** - Don't put too much logic in a single listener
5. **Type safety first** - Let TypeScript guide you to correct payload structures

## Adding New Event Types

1. Add the constant to `EVENT_TYPES` in `eventTypes.ts`
2. Add the event type to the `ChatEvent` discriminated union
3. Update this README if needed

Example:

```ts
// In eventTypes.ts
export const EVENT_TYPES = {
  // ... existing types
  NEW_EVENT: 'new:event',
} as const;

export type ChatEvent =
  // ... existing events
  | { type: typeof EVENT_TYPES.NEW_EVENT; data: string };
```

## Testing

The event system is fully tested. See:
- `__tests__/eventBus.test.ts` - Event bus unit tests
- `__tests__/integration.test.tsx` - Integration tests
- `../../hooks/__tests__/useEventBus.test.tsx` - React hook tests

Run tests with:
```bash
npm test
```

