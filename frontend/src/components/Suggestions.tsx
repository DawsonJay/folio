import { useState } from 'react';
import { useEvent, useEmit } from '../hooks/useEventBus';
import { EVENT_TYPES } from '../events/eventTypes';
import type { Suggestion } from '../types';

export default function Suggestions() {
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [initialSuggestions, setInitialSuggestions] = useState<Suggestion[]>([]);
  const emit = useEmit();

  useEvent(EVENT_TYPES.CHAT_QUESTION_ASKED, () => {
    setSuggestions([]);
  });

  useEvent(EVENT_TYPES.INITIAL_SUGGESTIONS_RECEIVED, (event) => {
    setSuggestions(event.suggestions);
    setInitialSuggestions(event.suggestions);
  });

  useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, (event) => {
    setSuggestions(event.suggestions);
  });

  useEvent(EVENT_TYPES.CHAT_ERROR, () => {
    if (initialSuggestions.length > 0) {
      setSuggestions(initialSuggestions);
    }
  });

  const handleSuggestionClick = (suggestion: Suggestion) => {
    if (suggestions.length === 0) {
      return;
    }
    emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: suggestion.text });
  };

  if (suggestions.length === 0) {
    const skeletonWidths = ['80px', '120px', '100px', '140px', '110px', '130px'];
    return (
      <div className="suggestions">
        {Array.from({ length: 6 }).map((_, index) => (
          <div
            key={index}
            className="suggestion-chip suggestion-skeleton"
            style={{ width: skeletonWidths[index] }}
          />
        ))}
      </div>
    );
  }

  return (
    <div className="suggestions">
      {suggestions.map((suggestion, index) => (
        <button
          key={index}
          className="suggestion-chip"
          onClick={() => handleSuggestionClick(suggestion)}
          type="button"
        >
          {suggestion.text}
        </button>
      ))}
    </div>
  );
}

