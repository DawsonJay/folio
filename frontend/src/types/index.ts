export interface Suggestion {
  text: string;
  query?: string;
}

export interface ProjectLinks {
  demo?: string;
  github?: string;
}

export interface APIResponse {
  answer: string;
  emotion: 'happy' | 'thinking' | 'surprised' | 'derp' | 'tired' | 'annoyed';
  suggestions: Suggestion[];
  projectLinks?: Record<string, ProjectLinks>;
  confidence?: string;
  top_score?: number;
}

