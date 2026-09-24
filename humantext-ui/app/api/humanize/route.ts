import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const response = await fetch('http://127.0.0.1:8000/api/v1/humanize/v5', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      // Set a generous timeout to allow local LLMs to finish
      signal: AbortSignal.timeout(120000),
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { error: data.detail || 'Backend processing error' },
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch (err: any) {
    console.error('Humanize proxy error:', err);
    return NextResponse.json(
      { 
        error: 'Unable to connect to HumanText backend. Please ensure the backend server is running on port 8000.',
        detail: err?.message || String(err)
      },
      { status: 502 }
    );
  }
}
