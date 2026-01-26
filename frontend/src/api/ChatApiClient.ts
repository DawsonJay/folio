import { eventBus } from '../events/eventBus';
import { EVENT_TYPES } from '../events/eventTypes';
import { fetchInitialSuggestions, sendQuestion } from './chatApi';

class ChatApiClient {
  private static instance: ChatApiClient;
  private initialized = false;
  private unsubscribeQuestionAsked?: () => void;

  private constructor() {}

  static getInstance(): ChatApiClient {
    if (!ChatApiClient.instance) {
      ChatApiClient.instance = new ChatApiClient();
    }
    return ChatApiClient.instance;
  }

  initialize(): void {
    if (this.initialized) {
      return;
    }

    this.initialized = true;

    this.unsubscribeQuestionAsked = eventBus.on(
      EVENT_TYPES.CHAT_QUESTION_ASKED,
      (event) => {
        this.handleQuestionAsked(event);
      }
    );

    this.fetchInitialSuggestions();
  }

  private async fetchInitialSuggestions(): Promise<void> {
    try {
      const suggestions = await fetchInitialSuggestions();
      eventBus.emit(EVENT_TYPES.INITIAL_SUGGESTIONS_RECEIVED, {
        suggestions,
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to fetch suggestions';
      eventBus.emit(EVENT_TYPES.CHAT_ERROR, { error: errorMessage });
    }
  }

  private async handleQuestionAsked(
    event: Extract<
      import('../events/eventTypes').ChatEvent,
      { type: typeof EVENT_TYPES.CHAT_QUESTION_ASKED }
    >
  ): Promise<void> {
    try {
      const response = await sendQuestion(event.question);
      eventBus.emit(EVENT_TYPES.CHAT_RESPONSE_RECEIVED, {
        answer: response.answer,
        suggestions: response.suggestions,
      });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to send question';
      eventBus.emit(EVENT_TYPES.CHAT_ERROR, { error: errorMessage });
    }
  }

  destroy(): void {
    if (this.unsubscribeQuestionAsked) {
      this.unsubscribeQuestionAsked();
      this.unsubscribeQuestionAsked = undefined;
    }
    this.initialized = false;
  }
}

export const chatApiClient = ChatApiClient.getInstance();

