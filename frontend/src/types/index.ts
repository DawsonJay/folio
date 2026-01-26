export interface Suggestion {
  text: string;
}

export interface APIResponse {
  answer: string;
  suggestions: Suggestion[];
}

