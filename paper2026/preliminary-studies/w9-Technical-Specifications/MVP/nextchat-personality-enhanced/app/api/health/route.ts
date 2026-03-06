/**
 * NextChat-Enhanced: System Health Check API Route
 * Monitors Phase 1 multi-agent system health
 */

import { NextRequest, NextResponse } from "next/server";

const PHASE1_API_URL = process.env.PHASE1_API_URL || "http://localhost:3001";
const PHASE1_API_KEY = process.env.PHASE1_API_KEY || "";
const N8N_URL = process.env.N8N_URL || "http://localhost:5678";

interface SystemHealth {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  version: string;
  service: string;
  services: {
    api: 'healthy' | 'degraded' | 'unhealthy';
    database: 'healthy' | 'degraded' | 'unhealthy'; 
    n8n: 'healthy' | 'degraded' | 'unhealthy';
    personality: 'healthy' | 'degraded' | 'unhealthy';
    agents: 'healthy' | 'degraded' | 'unhealthy';
  };
  performance: {
    response_time: number;
    memory_usage: any;
    uptime: number;
  };
  features: {
    personality_detection: boolean;
    ema_smoothing: boolean;
    verification_pipeline: boolean;
    multi_agent_coordination: boolean;
    real_time_updates: boolean;
  };
  agent_status: {
    detector: 'active' | 'idle' | 'error';
    regulator: 'active' | 'idle' | 'error';
    generator: 'active' | 'idle' | 'error';
    verifier: 'active' | 'idle' | 'error';
    coordinator: 'active' | 'idle' | 'error';
  };
  diagnostics?: {
    phase1_api: any;
    n8n_status: any;
    database_connection: any;
  };
}

export async function GET(req: NextRequest) {
  const startTime = Date.now();
  
  try {
    // Check Phase 1 API health
    const phase1Health = await checkPhase1ApiHealth();
    
    // Check N8N health
    const n8nHealth = await checkN8nHealth();
    
    // Determine overall system status
    const overallStatus = determineOverallStatus(phase1Health, n8nHealth);
    
    const responseTime = Date.now() - startTime;
    
    const healthData: SystemHealth = {
      status: overallStatus,
      timestamp: new Date().toISOString(),
      version: process.env.NEXTCHAT_PERSONALITY_VERSION || "2.16.1-personality-v1.0",
      service: "nextchat-personality-enhanced",
      
      services: {
        api: phase1Health.api || 'unhealthy',
        database: phase1Health.database || 'unhealthy',
        n8n: n8nHealth.status || 'unhealthy',
        personality: phase1Health.personality || 'unhealthy',
        agents: phase1Health.agents || 'unhealthy',
      },
      
      performance: {
        response_time: responseTime,
        memory_usage: getMemoryUsage(),
        uptime: process.uptime(),
      },
      
      features: {
        personality_detection: phase1Health.api === 'healthy',
        ema_smoothing: phase1Health.personality === 'healthy',
        verification_pipeline: phase1Health.agents === 'healthy',
        multi_agent_coordination: phase1Health.agents === 'healthy' && n8nHealth.status === 'healthy',
        real_time_updates: true, // Frontend feature
      },
      
      agent_status: phase1Health.agent_details || {
        detector: 'idle',
        regulator: 'idle',
        generator: 'idle',
        verifier: 'idle',
        coordinator: 'idle',
      },
      
      diagnostics: {
        phase1_api: phase1Health.details,
        n8n_status: n8nHealth.details,
        database_connection: phase1Health.database_details,
      },
    };
    
    // Return appropriate HTTP status based on health
    const httpStatus = overallStatus === 'healthy' ? 200 : 
                      overallStatus === 'degraded' ? 200 : 503;
    
    return NextResponse.json(healthData, { status: httpStatus });
    
  } catch (error) {
    console.error("Health check failed:", error);
    
    const errorHealth: SystemHealth = {
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      version: process.env.NEXTCHAT_PERSONALITY_VERSION || "2.16.1-personality-v1.0",
      service: "nextchat-personality-enhanced",
      
      services: {
        api: 'unhealthy',
        database: 'unhealthy',
        n8n: 'unhealthy',
        personality: 'unhealthy',
        agents: 'unhealthy',
      },
      
      performance: {
        response_time: Date.now() - startTime,
        memory_usage: getMemoryUsage(),
        uptime: process.uptime(),
      },
      
      features: {
        personality_detection: false,
        ema_smoothing: false,
        verification_pipeline: false,
        multi_agent_coordination: false,
        real_time_updates: true,
      },
      
      agent_status: {
        detector: 'error',
        regulator: 'error', 
        generator: 'error',
        verifier: 'error',
        coordinator: 'error',
      },
      
      diagnostics: {
        phase1_api: { error: error instanceof Error ? error.message : "Unknown error" },
        n8n_status: { error: "Connection failed" },
        database_connection: { error: "Connection failed" },
      },
    };
    
    return NextResponse.json(errorHealth, { status: 503 });
  }
}

// Simple health endpoint for load balancers
export async function HEAD() {
  try {
    // Quick health check - just verify Phase 1 API is reachable
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2000);
    
    const response = await fetch(`${PHASE1_API_URL}/api/health`, {
      method: 'HEAD',
      signal: controller.signal,
      headers: {
        ...(PHASE1_API_KEY && { Authorization: `Bearer ${PHASE1_API_KEY}` }),
      },
    });
    
    clearTimeout(timeoutId);
    
    return new Response(null, { status: response.ok ? 200 : 503 });
    
  } catch (error) {
    return new Response(null, { status: 503 });
  }
}

// Helper functions
async function checkPhase1ApiHealth(): Promise<any> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);
    
    const response = await fetch(`${PHASE1_API_URL}/api/health`, {
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(PHASE1_API_KEY && { Authorization: `Bearer ${PHASE1_API_KEY}` }),
      },
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      return {
        api: 'degraded',
        database: 'unknown',
        personality: 'unknown',
        agents: 'unknown',
        details: { error: `HTTP ${response.status}` },
      };
    }
    
    const healthData = await response.json();
    
    return {
      api: healthData.status === 'healthy' ? 'healthy' : 'degraded',
      database: healthData.services?.database === 'healthy' ? 'healthy' : 'degraded',
      personality: healthData.services?.api === 'healthy' ? 'healthy' : 'degraded',
      agents: healthData.services?.n8n === 'healthy' ? 'healthy' : 'degraded',
      agent_details: healthData.agent_status || {},
      details: healthData,
      database_details: healthData.services || {},
    };
    
  } catch (error) {
    return {
      api: 'unhealthy',
      database: 'unknown',
      personality: 'unknown',
      agents: 'unknown', 
      details: { error: error instanceof Error ? error.message : "Connection failed" },
    };
  }
}

async function checkN8nHealth(): Promise<any> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);
    
    // N8N doesn't have a standard health endpoint, so we check the root
    const response = await fetch(N8N_URL, {
      method: 'HEAD',
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);
    
    return {
      status: response.ok ? 'healthy' : 'degraded',
      details: { status_code: response.status },
    };
    
  } catch (error) {
    return {
      status: 'unhealthy',
      details: { error: error instanceof Error ? error.message : "Connection failed" },
    };
  }
}

function determineOverallStatus(phase1Health: any, n8nHealth: any): 'healthy' | 'degraded' | 'unhealthy' {
  const criticalServices = [
    phase1Health.api,
    phase1Health.database,
    phase1Health.personality,
  ];
  
  const optionalServices = [
    phase1Health.agents,
    n8nHealth.status,
  ];
  
  // If any critical service is unhealthy, system is unhealthy
  if (criticalServices.includes('unhealthy')) {
    return 'unhealthy';
  }
  
  // If any critical service is degraded, or any optional service is unhealthy, system is degraded
  if (criticalServices.includes('degraded') || optionalServices.includes('unhealthy')) {
    return 'degraded';
  }
  
  // If any optional service is degraded, system is degraded
  if (optionalServices.includes('degraded')) {
    return 'degraded';
  }
  
  // All services healthy
  return 'healthy';
}

function getMemoryUsage(): any {
  if (typeof process !== 'undefined' && process.memoryUsage) {
    const usage = process.memoryUsage();
    return {
      rss: Math.round(usage.rss / 1024 / 1024) + ' MB',
      heapTotal: Math.round(usage.heapTotal / 1024 / 1024) + ' MB', 
      heapUsed: Math.round(usage.heapUsed / 1024 / 1024) + ' MB',
      external: Math.round(usage.external / 1024 / 1024) + ' MB',
    };
  }
  return { error: "Memory usage not available" };
}

















































