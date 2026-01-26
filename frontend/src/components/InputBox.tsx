import { useState, useRef, FormEvent } from 'react';
import { useEvent, useEmit } from '../hooks/useEventBus';
import { EVENT_TYPES } from '../events/eventTypes';

export default function InputBox() {
  const [inputValue, setInputValue] = useState('');
  const [isDisabled, setIsDisabled] = useState(false);
  const submitButtonRef = useRef<HTMLButtonElement>(null);
  const emit = useEmit();

  useEvent(EVENT_TYPES.CHAT_QUESTION_ASKED, (event) => {
    setInputValue(event.question);
    setIsDisabled(true);
  });

  useEvent(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, () => {
    setIsDisabled(false);
    setInputValue('');
  });

  useEvent(EVENT_TYPES.CHAT_ERROR, () => {
    setIsDisabled(false);
    setInputValue('');
  });

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const trimmedValue = inputValue.trim();
    if (!trimmedValue || isDisabled) {
      return;
    }

    emit(EVENT_TYPES.CHAT_QUESTION_ASKED, { question: trimmedValue });
    
    if (submitButtonRef.current) {
      submitButtonRef.current.classList.add('clicked');
      setTimeout(() => {
        submitButtonRef.current?.classList.remove('clicked');
      }, 500);
    }
  };

  return (
    <form className="input-box" onSubmit={handleSubmit}>
      <input
        type="text"
        className="input-box-field"
        placeholder="What would you like to know?"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        disabled={isDisabled}
      />
      <button
        ref={submitButtonRef}
        type="submit"
        className="input-box-submit"
        disabled={isDisabled || !inputValue.trim()}
        aria-label="Submit question"
      >
        <svg
          className="input-box-icon"
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle cx="9" cy="9" r="6" stroke="currentColor" strokeWidth="1.5" />
          <path
            d="M13 13L17 17"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
          />
        </svg>
      </button>
    </form>
  );
}

