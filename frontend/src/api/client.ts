import { AnalysisRequest } from '../types';

export const API_BASE = '/api';

export async function fetchConfig() {
  const res = await fetch(`${API_BASE}/config`);
  if (!res.ok) throw new Error('Failed to fetch config');
  return res.json();
}

export async function fetchReports() {
  const res = await fetch(`${API_BASE}/reports`);
  if (!res.ok) throw new Error('Failed to fetch reports');
  return res.json();
}

export async function downloadReport(filename: string) {
  window.open(`${API_BASE}/reports/${filename}`, '_blank');
}

// Since SSE with POST body is tricky with native EventSource,
// we'll use fetch to POST and read the stream.
export async function startAnalysisStream(
  request: AnalysisRequest,
  onProgress: (data: any) => void,
  onResult: (data: any) => void,
  onError: (err: any) => void
) {
  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    if (!reader) throw new Error('No reader available');

    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n\n');
      buffer = lines.pop() || '';

      for (const block of lines) {
        if (!block.trim()) continue;
        const eventMatch = block.match(/event: (.*)\n/);
        const dataMatch = block.match(/data: (.*)/);

        if (eventMatch && dataMatch) {
          const event = eventMatch[1];
          const dataStr = dataMatch[1];
          try {
            const data = JSON.parse(dataStr);
            if (event === 'progress') {
              onProgress(data);
            } else if (event === 'result') {
              onResult(data);
            } else if (event === 'error') {
              onError(data);
            }
          } catch (e) {
            console.error('Error parsing SSE data', e);
          }
        }
      }
    }
  } catch (err) {
    onError(err);
  }
}
