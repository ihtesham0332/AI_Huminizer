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
