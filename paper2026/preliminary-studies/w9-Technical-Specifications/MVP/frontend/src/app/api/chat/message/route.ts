import { NextRequest, NextResponse } from 'next/server';

// N8N Webhook URL
const N8N_WEBHOOK_URL = process.env.N8N_WEBHOOK_URL || 'http://localhost:5678/webhook/personality-chat-enhanced';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { session_id, message } = body;

    if (!message) {
      return NextResponse.json(
        { error: 'Message is required' },
        { status: 400 }
      );
    }

    // Forward the request to N8N webhook with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
    
    const requestBody = {
      session_id: session_id || crypto.randomUUID(), // Use proper UUID format for N8N compatibility
      turn_index: 1,
      message: message,
    };
    
    console.log('Sending to N8N:', N8N_WEBHOOK_URL, JSON.stringify(requestBody));
    
    let n8nResponse;
    try {
      n8nResponse = await fetch(N8N_WEBHOOK_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal,
      });
    } catch (fetchError) {
      clearTimeout(timeoutId);
      console.error('N8N fetch error:', fetchError);
      return NextResponse.json(
        { 
          error: 'Failed to reach N8N webhook',
          details: fetchError instanceof Error ? fetchError.message : 'Unknown error'
        },
        { status: 503 }
      );
    } finally {
      clearTimeout(timeoutId);
    }

    if (!n8nResponse.ok) {
      const errorText = await n8nResponse.text();
      console.error('N8N webhook error:', errorText);
      return NextResponse.json(
        { 
          error: 'Failed to process message',
          details: errorText 
        },
        { status: 500 }
      );
    }

    // Get response text first to handle empty responses
    const responseText = await n8nResponse.text();
    console.log('N8N response length:', responseText.length);
    
    if (!responseText || responseText.trim().length === 0) {
      console.error('N8N returned empty response');
      return NextResponse.json(
        { 
          error: 'N8N returned empty response',
          details: 'The workflow may not be configured correctly'
        },
        { status: 500 }
      );
    }

    let data;
    try {
      data = JSON.parse(responseText);
      console.log('N8N response OCEAN values:', JSON.stringify(data.personality_state?.ocean));
      console.log('N8N response pipeline_status:', JSON.stringify(data.pipeline_status));
    } catch (parseError) {
      console.error('Failed to parse N8N response:', responseText.substring(0, 200));
      return NextResponse.json(
        { 
          error: 'Invalid JSON response from N8N',
          details: parseError instanceof Error ? parseError.message : 'Unknown error'
        },
        { status: 500 }
      );
    }

    // Return the response in the format the frontend expects
    return NextResponse.json({
      session_id: data.session_id,
      message: {
        role: 'assistant',
        content: data.reply || data.message?.content || 'I apologize, but I encountered an issue processing your message.',
        timestamp: new Date().toISOString(),
      },
      personality_state: data.personality_state || {
        ocean: { O: 0, C: 0, E: 0, A: 0, N: 0 },
        confidence: {},
        stable: false,
        ema_applied: false,
      },
      regulation: data.regulation || {
        directives: [],
        analysis: {},
      },
      verification: data.verification || {
        status: 'unknown',
        adherence_score: 0,
        refinement_applied: false,
      },
      pipeline_status: data.pipeline_status || {
        detector: 'unknown',
        regulator: 'unknown',
        generator: 'unknown',
        verifier: 'unknown',
        database: 'unknown',
      },
    });
  } catch (error) {
    console.error('API route error:', error);
    return NextResponse.json(
      { 
        error: 'Internal server error',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json(
    { message: 'Chat API is running. Use POST to send messages.' },
    { status: 200 }
  );
}
