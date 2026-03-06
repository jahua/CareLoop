import { NextRequest, NextResponse } from 'next/server';

// N8N Webhook URL
const N8N_WEBHOOK_URL = process.env.N8N_WEBHOOK_URL || 'http://localhost:5678/webhook/personality-chat-enhanced';
const NVIDIA_API_URL = process.env.NVIDIA_API_URL || 'https://integrate.api.nvidia.com/v1/chat/completions';
const NVIDIA_API_KEY = process.env.NVIDIA_API_KEY || '';
const NVIDIA_MODEL = process.env.NVIDIA_MODEL || 'meta/llama-3.1-8b-instruct';

async function buildNvidiaRecoveryResponse(sessionId: string, userMessage: string, reason: string) {
  if (!NVIDIA_API_KEY) {
    return buildFallbackResponse(sessionId, `${reason}_missing_nvidia_key`);
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 12000);
    const response = await fetch(NVIDIA_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${NVIDIA_API_KEY}`,
        },
        signal: controller.signal,
        body: JSON.stringify({
          model: NVIDIA_MODEL,
          messages: [
            {
              role: 'system',
              content: [
                'You are a supportive assistant and personality analyzer.',
                'Return ONLY strict JSON with keys: reply, ocean, confidence.',
                'ocean must include O,C,E,A,N as numbers in [-1,1].',
                'confidence must include O,C,E,A,N as numbers in [0,1].',
                'Do not include markdown or any extra text.',
              ].join(' '),
            },
            {
              role: 'user',
              content: String(userMessage || '').trim() || 'Hello',
            },
          ],
          temperature: 0.2,
          max_tokens: 320,
        }),
      });
    clearTimeout(timeoutId);

    if (!response.ok) {
      return buildFallbackResponse(sessionId, `${reason}_nvidia_http_${response.status}`);
    }

    const data = await response.json();
    const content = data?.choices?.[0]?.message?.content;
    if (!content || typeof content !== 'string') {
      return buildFallbackResponse(sessionId, `${reason}_nvidia_invalid_payload`);
    }

    let parsed: any = null;
    try {
      parsed = JSON.parse(content.trim());
    } catch {
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        try {
          parsed = JSON.parse(jsonMatch[0]);
        } catch {
          parsed = null;
        }
      }
    }

    if (!parsed || typeof parsed !== 'object') {
      return buildFallbackResponse(sessionId, `${reason}_nvidia_invalid_json`);
    }

    const safeOcean = {
      O: Number(parsed?.ocean?.O ?? 0),
      C: Number(parsed?.ocean?.C ?? 0),
      E: Number(parsed?.ocean?.E ?? 0),
      A: Number(parsed?.ocean?.A ?? 0),
      N: Number(parsed?.ocean?.N ?? 0),
    };
    const safeConfidence = {
      O: Number(parsed?.confidence?.O ?? 0),
      C: Number(parsed?.confidence?.C ?? 0),
      E: Number(parsed?.confidence?.E ?? 0),
      A: Number(parsed?.confidence?.A ?? 0),
      N: Number(parsed?.confidence?.N ?? 0),
    };
    const safeReply = typeof parsed?.reply === 'string' && parsed.reply.trim().length > 0
      ? parsed.reply.trim()
      : content.trim();

    return {
      session_id: sessionId,
      message: {
        role: 'assistant',
        content: safeReply,
        timestamp: new Date().toISOString(),
      },
      personality_state: {
        ocean: safeOcean,
        confidence: safeConfidence,
        stable: true,
        ema_applied: false,
      },
      regulation: {
        directives: [],
        analysis: { source: 'nvidia_recovery' },
      },
      verification: {
        status: 'recovered',
        adherence_score: 0,
        refinement_applied: false,
      },
      pipeline_status: {
        detector: 'nvidia_recovery',
        regulator: 'bypassed',
        generator: 'nvidia_recovery',
        verifier: 'bypassed',
        database: reason,
      },
    };
  } catch (error) {
    return buildFallbackResponse(sessionId, `${reason}_nvidia_exception`);
  }
}

function buildFallbackResponse(sessionId: string, reason: string) {
  return {
    session_id: sessionId,
    message: {
      role: 'assistant',
      content: 'I can connect, but the workflow returned no valid response. Please verify your N8N workflow is active and returns JSON.',
      timestamp: new Date().toISOString(),
    },
    personality_state: {
      ocean: { O: 0, C: 0, E: 0, A: 0, N: 0 },
      confidence: {},
      stable: false,
      ema_applied: false,
    },
    regulation: {
      directives: [],
      analysis: {},
    },
    verification: {
      status: 'degraded',
      adherence_score: 0,
      refinement_applied: false,
    },
    pipeline_status: {
      detector: 'unknown',
      regulator: 'unknown',
      generator: 'unknown',
      verifier: 'unknown',
      database: reason,
    },
  };
}

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
      llm_provider: 'nvidia',
      llm_config: {
        api_url: NVIDIA_API_URL,
        model: NVIDIA_MODEL,
      },
    };
    
    console.log('Sending to N8N:', N8N_WEBHOOK_URL, JSON.stringify(requestBody));
    
    let n8nResponse;
    try {
      n8nResponse = await fetch(N8N_WEBHOOK_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-NVIDIA-API-URL': NVIDIA_API_URL,
          'X-NVIDIA-MODEL': NVIDIA_MODEL,
          ...(NVIDIA_API_KEY ? { 'X-NVIDIA-API-KEY': NVIDIA_API_KEY } : {}),
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal,
      });
    } catch (fetchError) {
      clearTimeout(timeoutId);
      console.error('N8N fetch error:', fetchError);
      return NextResponse.json(await buildNvidiaRecoveryResponse(requestBody.session_id, message, 'n8n_unreachable'));
    } finally {
      clearTimeout(timeoutId);
    }

    if (!n8nResponse.ok) {
      const errorText = await n8nResponse.text();
      console.error('N8N webhook error:', errorText);
      return NextResponse.json(await buildNvidiaRecoveryResponse(requestBody.session_id, message, `n8n_http_${n8nResponse.status}`));
    }

    // Get response text first to handle empty responses
    const responseText = await n8nResponse.text();
    console.log('N8N response length:', responseText.length);
    
    if (!responseText || responseText.trim().length === 0) {
      console.error('N8N returned empty response');
      return NextResponse.json(await buildNvidiaRecoveryResponse(requestBody.session_id, message, 'n8n_empty_response'));
    }

    let data;
    try {
      data = JSON.parse(responseText);
      console.log('N8N response OCEAN values:', JSON.stringify(data.personality_state?.ocean));
      console.log('N8N response pipeline_status:', JSON.stringify(data.pipeline_status));
    } catch (parseError) {
      console.error('Failed to parse N8N response:', responseText.substring(0, 200));
      return NextResponse.json(await buildNvidiaRecoveryResponse(requestBody.session_id, message, 'n8n_invalid_json'));
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
