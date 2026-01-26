import type { APIResponse, Suggestion } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorText = await response.text().catch(() => 'Unknown error');
    throw new Error(`API error: ${response.status} ${errorText}`);
  }
  return response.json();
}

export async function fetchInitialSuggestions(): Promise<Suggestion[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/suggestions`);
    const data = await handleResponse<{ suggestions: Suggestion[] }>(response);
    return data.suggestions;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to fetch suggestions: ${error.message}`);
    }
    throw new Error('Failed to fetch suggestions: Unknown error');
  }
}

export async function sendQuestion(question: string): Promise<APIResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question }),
    });
    return handleResponse<APIResponse>(response);
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to send question: ${error.message}`);
    }
    throw new Error('Failed to send question: Unknown error');
  }
}

