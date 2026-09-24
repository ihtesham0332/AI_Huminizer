export interface HumanizeRequest {
  text: string;
  document_type?: string;
  target_mode?: string;
  target_tone?: string;
  target_audience?: string;
}

export interface HumanizeResponse {
  request_id: string;
  original_text: string;
  humanized_text: string;
  quality_score: number;
  naturalness_score: number;
  status: string;
  metadata?: any;
}

const API_URL = 'http://localhost:8000/api/v1/humanize';

export async function humanizeText(payload: HumanizeRequest): Promise<HumanizeResponse> {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail?.[0]?.msg || `API error: ${response.status}`);
  }

  return response.json();
}

export async function* streamHumanizeText(payload: HumanizeRequest) {
  const response = await fetch(`${API_URL}/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'text/event-stream'
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  const reader = response.body?.getReader();
  if (!reader) throw new Error("Stream not supported");
  const decoder = new TextDecoder("utf-8");

  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    
    const lines = buffer.split('\n');
    buffer = lines.pop() || ""; // Keep the incomplete line in the buffer
    
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const dataStr = line.slice(6);
        if (!dataStr.trim()) continue;
        try {
          const data = JSON.parse(dataStr);
          yield data;
        } catch (e) {
          console.error("Error parsing stream chunk", e);
        }
      }
    }
  }
}

export async function rewriteSentence(sentence: string, context: string, tone: string) {
  const response = await fetch(`${API_URL}/sentence`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sentence, context, tone })
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  const data = await response.json();
  return data.variations;
}
export async function scanTextProbability(text: string) {
  const response = await fetch(`${API_URL}/scan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}
