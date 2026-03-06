// Enhanced types for Phase 1 Multi-Agent Personality System

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
  agentId?: string;
  metadata?: {
    processingTime?: number;
    confidence?: number;
    refinementApplied?: boolean;
    emotionalState?: string;
  };
}

export interface PersonalityState {
  ocean: {
    O: number; // Openness
    C: number; // Conscientiousness  
    E: number; // Extraversion
    A: number; // Agreeableness
    N: number; // Neuroticism
  };
  ocean_raw?: {
    O: number;
    C: number;
    E: number;
    A: number;
    N: number;
  };
  stable: boolean;
  confidence_scores: {
    O: number;
    C: number;
    E: number;
    A: number;
    N: number;
  };
  policy_plan: string[];
  ema_applied?: boolean;
  ema_alpha?: number;
  turn_number?: number;
  stabilization_turns?: number;
}

export interface Agent {
  id: string;
  name: string;
  role: 'detector' | 'regulator' | 'generator' | 'verifier' | 'coordinator';
  status: 'active' | 'idle' | 'processing' | 'error';
  model: string;
  lastActivity?: string;
  personalityFocus: 'OCEAN' | 'therapeutic' | 'crisis' | 'general';
  performance: {
    successRate: number;
    averageProcessingTime: number;
    totalProcessed: number;
  };
  capabilities: string[];
}

export interface VerificationResult {
  status: 'verified' | 'refined' | 'needs_refinement';
  adherence_score: number;
  original_score?: number;
  refinement_applied: boolean;
  issues_identified: string[];
  criterion_scores: {
    directive_adherence: number;
    personality_consistency: number;
    therapeutic_appropriateness: number;
    grounding: number;
    length_constraint: number;
  };
}

export interface SessionState {
  session_id: string;
  created_at: string;
  total_turns: number;
  personality_state: PersonalityState;
  verification_stats: {
    average_adherence: number;
    refinements_applied: number;
    total_verified: number;
  };
  agents_involved: string[];
  conversation_summary?: string;
}

export interface ApiResponse {
  session_id: string;
  reply: string;
  user_message: string;
  personality_state: PersonalityState;
  regulation: {
    directives: string[];
    analysis: any;
  };
  verification: VerificationResult;
  pipeline_status: {
    detector: string;
    regulator: string;
    generator: string;
    verifier: string;
    database: string;
  };
  api_metadata: {
    response_time: string;
    version: string;
    pipeline_type: string;
    turn_index: number;
  };
}

export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'unhealthy';
  services: {
    api: string;
    database: string;
    n8n: string;
  };
  timestamp: string;
  version: string;
}

export interface AgentActivity {
  agentId: string;
  action: string;
  timestamp: string;
  duration?: number;
  success: boolean;
  details?: any;
}

export interface ConversationInsights {
  emotionalJourney: Array<{
    turn: number;
    emotional_state: string;
    intensity: number;
    timestamp: string;
  }>;
  personalityEvolution: Array<{
    turn: number;
    ocean: PersonalityState['ocean'];
    confidence: PersonalityState['confidence_scores'];
    ema_applied: boolean;
  }>;
  therapeuticProgress: {
    directivesUsed: string[];
    adaptationQuality: number;
    clientEngagement: number;
    breakthroughMoments: string[];
  };
}

export interface MultiAgentConfig {
  emaSettings: {
    alpha: number;
    confidenceThreshold: number;
    stabilizationTurns: number;
  };
  verificationSettings: {
    minAdherenceScore: number;
    maxRefinementAttempts: number;
    enableAutomaticRefinement: boolean;
  };
  agentCoordination: {
    enableParallelProcessing: boolean;
    timeoutMs: number;
    retryAttempts: number;
  };
}
