export function logEvent(eventType: string): void {
  if (import.meta.env.VITE_ENABLE_EVENT_LOGGING !== 'true') {
    return;
  }

  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${eventType}`);
}

