/**
 * NextChat-Enhanced: Phase 1 Personality Detection Store
 * Integrated with NextChat's Zustand architecture patterns
 */

import { createPersistStore } from "../utils/store";
import { nanoid } from "nanoid";
import { StoreKey } from "../constant";

export type PersonalityTrait = 'O' | 'C' | 'E' | 'A' | 'N';

export interface PersonalityOcean {
  O: number; // Openness: -1 (low) to 1 (high)
  C: number; // Conscientiousness: -1 (low) to 1 (high)
  E: number; // Extraversion: -1 (low) to 1 (high)
  A: number; // Agreeableness: -1 (low) to 1 (high)
  N: number; // Neuroticism: -1 (low) to 1 (high)
}

export interface PersonalityConfidence {
  O: number; // 0.0 to 1.0
  C: number; // 0.0 to 1.0
  E: number; // 0.0 to 1.0
  A: number; // 0.0 to 1.0
  N: number; // 0.0 to 1.0
}

export interface PersonalityState {
  // Core OCEAN personality traits
  ocean: PersonalityOcean;
  ocean_raw?: PersonalityOcean; // Raw detection before EMA smoothing
  
  // Confidence scores for each trait
  confidence_scores: PersonalityConfidence;
  
  // EMA Smoothing state
  ema_applied: boolean;
  ema_alpha: number;
  stable: boolean;
  stabilization_turns: number;
  turn_number: number;
  
  // Therapeutic directives
  policy_plan: string[];
  
  // Detection metadata
  last_updated: string;
  detection_history: PersonalitySnapshot[];
  
  // Verification pipeline
  verification_stats: {
    average_adherence: number;
    refinements_applied: number;
    total_verified: number;
    last_score?: number;
  };
  
  // Emotional context
  emotional_state?: string;
  emotional_intensity?: number;
}

export interface PersonalitySnapshot {
  timestamp: string;
  turn: number;
  ocean: PersonalityOcean;
  confidence: PersonalityConfidence;
  ema_applied: boolean;
  emotional_state?: string;
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

export interface AgentActivity {
  agentId: string;
  action: string;
  timestamp: string;
  duration?: number;
  success: boolean;
  details?: any;
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

export interface ConversationInsights {
  emotionalJourney: Array<{
    turn: number;
    emotional_state: string;
    intensity: number;
    timestamp: string;
  }>;
  personalityEvolution: Array<{
    turn: number;
    ocean: PersonalityOcean;
    confidence: PersonalityConfidence;
    ema_applied: boolean;
  }>;
  therapeuticProgress: {
    directivesUsed: string[];
    adaptationQuality: number;
    clientEngagement: number;
    breakthroughMoments: string[];
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

export interface PersonalityStore {
  // Personality State
  personalityState: PersonalityState;
  
  // Multi-Agent System
  agents: Agent[];
  agentActivities: AgentActivity[];
  activeAgents: string[];
  
  // System Health
  systemHealth: SystemHealth | null;
  isPersonalityEnabled: boolean;
  
  // Insights & Analytics
  conversationInsights: ConversationInsights | null;
  
  // Actions
  updatePersonalityState: (state: Partial<PersonalityState>) => void;
  addPersonalitySnapshot: (snapshot: PersonalitySnapshot) => void;
  updateAgentStatus: (agentId: string, status: Agent['status']) => void;
  addAgentActivity: (activity: AgentActivity) => void;
  updateSystemHealth: (health: SystemHealth) => void;
  resetPersonalityState: () => void;
  enablePersonality: (enabled: boolean) => void;
  
  // Phase 1 API Integration
  detectPersonality: (message: string, sessionId: string) => Promise<PersonalityState>;
  getPersonalityInsights: (sessionId: string) => Promise<ConversationInsights>;
  checkSystemHealth: () => Promise<SystemHealth>;
}

const DEFAULT_PERSONALITY_STATE: PersonalityState = {
  ocean: { O: 0, C: 0, E: 0, A: 0, N: 0 },
  confidence_scores: { O: 0, C: 0, E: 0, A: 0, N: 0 },
  ema_applied: false,
  ema_alpha: 0.3,
  stable: false,
  stabilization_turns: 5,
  turn_number: 0,
  policy_plan: [],
  last_updated: new Date().toISOString(),
  detection_history: [],
  verification_stats: {
    average_adherence: 0,
    refinements_applied: 0,
    total_verified: 0,
  },
};

const DEFAULT_AGENTS: Agent[] = [
  {
    id: 'personality-detector',
    name: 'Personality Detection Agent',
    role: 'detector',
    status: 'idle',
    model: 'gpt-4-enhanced-ema',
    personalityFocus: 'OCEAN',
    performance: { successRate: 0, averageProcessingTime: 0, totalProcessed: 0 },
    capabilities: ['EMA Smoothing', 'Confidence Weighting', 'Zurich Model Integration'],
  },
  {
    id: 'behavioral-regulator',
    name: 'Behavioral Regulation Agent',
    role: 'regulator',
    status: 'idle',
    model: 'zurich-model-enhanced',
    personalityFocus: 'therapeutic',
    performance: { successRate: 0, averageProcessingTime: 0, totalProcessed: 0 },
    capabilities: ['Directive Mapping', 'Confidence Weighting', 'Therapeutic Guidelines'],
  },
  {
    id: 'response-generator',
    name: 'Response Generation Agent',
    role: 'generator',
    status: 'idle',
    model: 'gpt-4-therapeutic',
    personalityFocus: 'general',
    performance: { successRate: 0, averageProcessingTime: 0, totalProcessed: 0 },
    capabilities: ['Personality-Aware Responses', 'Therapeutic Communication', 'Contextual Adaptation'],
  },
  {
    id: 'quality-verifier',
    name: 'Quality Verification Agent',
    role: 'verifier',
    status: 'idle',
    model: 'gpt-4-verification',
    personalityFocus: 'general',
    performance: { successRate: 0, averageProcessingTime: 0, totalProcessed: 0 },
    capabilities: ['Response Verification', 'Directive Adherence', 'Automatic Refinement'],
  },
  {
    id: 'session-coordinator',
    name: 'Session Coordination Agent',
    role: 'coordinator',
    status: 'idle',
    model: 'coordinator-enhanced',
    personalityFocus: 'therapeutic',
    performance: { successRate: 0, averageProcessingTime: 0, totalProcessed: 0 },
    capabilities: ['Session Management', 'Agent Coordination', 'Crisis Detection'],
  },
];

export const usePersonalityStore = createPersistStore(
  {
    personalityState: DEFAULT_PERSONALITY_STATE,
    agents: DEFAULT_AGENTS,
    agentActivities: [],
    activeAgents: [],
    systemHealth: null,
    isPersonalityEnabled: true,
    conversationInsights: null,

    updatePersonalityState: (state: Partial<PersonalityState>) =>
      void 0, // Implemented by createPersistStore
    
    addPersonalitySnapshot: (snapshot: PersonalitySnapshot) =>
      void 0,
    
    updateAgentStatus: (agentId: string, status: Agent['status']) =>
      void 0,
    
    addAgentActivity: (activity: AgentActivity) =>
      void 0,
    
    updateSystemHealth: (health: SystemHealth) =>
      void 0,
    
    resetPersonalityState: () =>
      void 0,
    
    enablePersonality: (enabled: boolean) =>
      void 0,

    // Phase 1 API Integration
    detectPersonality: async (message: string, sessionId: string) => {
      // Integration with Phase 1 API
      const apiUrl = process.env.NEXT_PUBLIC_PHASE1_API_URL || 'http://localhost:3001';
      
      try {
        const response = await fetch(`${apiUrl}/api/chat/message`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: sessionId, message }),
        });
        
        if (!response.ok) throw new Error('API request failed');
        
        const data = await response.json();
        return data.personality_state || DEFAULT_PERSONALITY_STATE;
      } catch (error) {
        console.error('Personality detection failed:', error);
        throw error;
      }
    },

    getPersonalityInsights: async (sessionId: string) => {
      const apiUrl = process.env.NEXT_PUBLIC_PHASE1_API_URL || 'http://localhost:3001';
      
      try {
        const response = await fetch(`${apiUrl}/api/personality/insights/${sessionId}`);
        if (!response.ok) throw new Error('Insights request failed');
        
        return await response.json();
      } catch (error) {
        console.error('Failed to get personality insights:', error);
        throw error;
      }
    },

    checkSystemHealth: async () => {
      const apiUrl = process.env.NEXT_PUBLIC_PHASE1_API_URL || 'http://localhost:3001';
      
      try {
        const response = await fetch(`${apiUrl}/api/health`);
        if (!response.ok) throw new Error('Health check failed');
        
        return await response.json();
      } catch (error) {
        console.error('System health check failed:', error);
        throw error;
      }
    },
  } as PersonalityStore,
  
  {
    name: StoreKey.PersonalityStore || "personality-store",
    version: 1,
    
    // Custom state transformations
    migrate: (persistedState: any, version: number) => {
      if (version === 0) {
        // Migration from v0 to v1
        return {
          ...persistedState,
          personalityState: {
            ...DEFAULT_PERSONALITY_STATE,
            ...persistedState.personalityState,
          },
          agents: DEFAULT_AGENTS,
        };
      }
      return persistedState;
    },
    
    // Only persist essential state, not temporary data
    partialize: (state: PersonalityStore) => ({
      personalityState: state.personalityState,
      isPersonalityEnabled: state.isPersonalityEnabled,
      // Don't persist agents, activities, or system health (they should be fresh on reload)
    }),
  }
);

// Helper functions for personality calculations
export const calculatePersonalityDistance = (state1: PersonalityOcean, state2: PersonalityOcean): number => {
  const traits: PersonalityTrait[] = ['O', 'C', 'E', 'A', 'N'];
  return Math.sqrt(
    traits.reduce((sum, trait) => {
      const diff = state1[trait] - state2[trait];
      return sum + diff * diff;
    }, 0)
  );
};

export const applyEmaSmoothing = (
  current: PersonalityOcean,
  previous: PersonalityOcean,
  alpha: number
): PersonalityOcean => {
  const traits: PersonalityTrait[] = ['O', 'C', 'E', 'A', 'N'];
  const smoothed: PersonalityOcean = { O: 0, C: 0, E: 0, A: 0, N: 0 };
  
  traits.forEach(trait => {
    smoothed[trait] = alpha * current[trait] + (1 - alpha) * previous[trait];
  });
  
  return smoothed;
};

export const getPersonalityTraitName = (trait: PersonalityTrait): string => {
  const names = {
    O: 'Openness',
    C: 'Conscientiousness', 
    E: 'Extraversion',
    A: 'Agreeableness',
    N: 'Neuroticism',
  };
  return names[trait];
};

export const getPersonalityTraitDescription = (trait: PersonalityTrait): string => {
  const descriptions = {
    O: 'Creativity, curiosity, willingness to try new things',
    C: 'Organization, discipline, goal-directed behavior',
    E: 'Social energy, assertiveness, positive emotions',
    A: 'Cooperation, trust, empathy for others',
    N: 'Emotional stability, stress resilience',
  };
  return descriptions[trait];
};

















































