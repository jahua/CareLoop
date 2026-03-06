import { NextResponse } from 'next/server';

const N8N_WEBHOOK_URL = process.env.N8N_WEBHOOK_URL || 'http://localhost:5678/webhook/personality-chat-enhanced';
const NVIDIA_API_URL = process.env.NVIDIA_API_URL || 'https://integrate.api.nvidia.com/v1/chat/completions';
const NVIDIA_MODEL = process.env.NVIDIA_MODEL || 'meta/llama-3.1-8b-instruct';
const NVIDIA_API_KEY_CONFIGURED = Boolean(process.env.NVIDIA_API_KEY);

async function checkN8NHealth(): Promise<string> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2000); // 2 second timeout
    
    const response = await fetch(N8N_WEBHOOK_URL, {
      method: 'GET',
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);
    
    // N8N webhook returns 404 for GET, which means it's running (only accepts POST)
    if (response.status === 404 || response.status === 405 || response.ok) {
      return 'healthy';
    }
    return 'degraded';
  } catch (error) {
    return 'unhealthy';
  }
}

async function checkDatabaseHealth(): Promise<string> {
  // We can't directly check PostgreSQL from the frontend API route
  // but we can infer it's healthy if N8N is working (N8N uses the DB)
  return 'unknown';
}

export async function GET() {
  try {
    const [n8nStatus, dbStatus] = await Promise.all([
      checkN8NHealth(),
      checkDatabaseHealth(),
    ]);

    const overallStatus = 
      n8nStatus === 'healthy' && (dbStatus === 'healthy' || dbStatus === 'unknown')
        ? 'healthy'
        : n8nStatus === 'unhealthy' || dbStatus === 'unhealthy'
        ? 'unhealthy'
        : 'degraded';

    const health = {
      status: overallStatus,
      services: {
        api: 'healthy', // Frontend API is running if we're here
        database: dbStatus,
        n8n: n8nStatus,
      },
      llm: {
        provider: 'nvidia',
        api_url: NVIDIA_API_URL,
        model: NVIDIA_MODEL,
        api_key_configured: NVIDIA_API_KEY_CONFIGURED,
      },
      timestamp: new Date().toISOString(),
      version: '1.0.0-phase1',
    };

    return NextResponse.json(health, { status: 200 });
  } catch (error) {
    console.error('Health check failed:', error);
    
    return NextResponse.json(
      {
        status: 'unhealthy',
        services: {
          api: 'healthy',
          database: 'unknown',
          n8n: 'unhealthy',
        },
        timestamp: new Date().toISOString(),
        version: '1.0.0-phase1',
      },
      { status: 500 }
    );
  }
}

export async function HEAD() {
  // For health check tools that use HEAD requests
  return new Response(null, { status: 200 });
}
