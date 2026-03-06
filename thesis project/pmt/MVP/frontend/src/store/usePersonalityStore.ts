import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { v4 as uuidv4 } from 'uuid';
import { 
  Message, 
  PersonalityState, 
  Agent, 
  SessionState, 
  VerificationResult,
  AgentActivity,
  ConversationInsights,
  SystemHealth 
} from '../types';

interface PersonalityStore {
  // Session State
  sessionId: string;
  messages: Message[];
  personalityState: PersonalityState;
  sessionState: SessionState | null;
  
  // Agent Management
  agents: Agent[];
  agentActivities: AgentActivity[];
  activeAgents: string[];
  
  // System State
  isLoading: boolean;
  connectionStatus: 'connecting' | 'connected' | 'error';
  systemHealth: SystemHealth | null;
  
  // Insights & Analytics
  conversationInsights: ConversationInsights | null;
  
  // Actions
  setSessionId: (id: string) => void;
  addMessage: (message: Message) => void;
  updatePersonalityState: (state: Partial<PersonalityState>) => void;
  setLoading: (loading: boolean) => void;
  setConnectionStatus: (status: 'connecting' | 'connected' | 'error') => void;
  updateAgentStatus: (agentId: string, status: Agent['status']) => void;
  addAgentActivity: (activity: AgentActivity) => void;
  updateSystemHealth: (health: SystemHealth) => void;
  clearSession: () => void;
  
  // API Actions
  sendMessage: (content: string) => Promise<void>;
  initializeAgents: () => void;
  fetchSessionHistory: () => Promise<void>;
}

const initialPersonalityState: PersonalityState = {
  ocean: { O: 0, C: 0, E: 0, A: 0, N: 0 },
  stable: false,
  confidence_scores: { O: 0, C: 0, E: 0, A: 0, N: 0 },
  policy_plan: [],
  ema_applied: false,
  turn_number: 0,
};

const defaultAgents: Agent[] = [
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

export const usePersonalityStore = create<PersonalityStore>()(
  devtools(
    (set, get) => ({
      // Initial State
      sessionId: '', // Initialize empty, will be set on client
      messages: [],
      personalityState: initialPersonalityState,
      sessionState: null,
      agents: defaultAgents,
      agentActivities: [],
      activeAgents: [],
      isLoading: false,
      connectionStatus: 'connecting',
      systemHealth: null,
      conversationInsights: null,

      // Actions
      setSessionId: (id: string) => {
        set({ sessionId: id }, false, 'setSessionId');
      },

      addMessage: (message: Message) => {
        set(
          (state) => ({
            messages: [...state.messages, message],
          }),
          false,
          'addMessage'
        );
      },

      updatePersonalityState: (newState: Partial<PersonalityState>) => {
        set(
          (state) => ({
            personalityState: { ...state.personalityState, ...newState },
          }),
          false,
          'updatePersonalityState'
        );
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading }, false, 'setLoading');
      },

      setConnectionStatus: (status: 'connecting' | 'connected' | 'error') => {
        set({ connectionStatus: status }, false, 'setConnectionStatus');
      },

      updateAgentStatus: (agentId: string, status: Agent['status']) => {
        set(
          (state) => ({
            agents: state.agents.map((agent) =>
              agent.id === agentId
                ? { ...agent, status, lastActivity: new Date().toISOString() }
                : agent
            ),
          }),
          false,
          'updateAgentStatus'
        );
      },

      addAgentActivity: (activity: AgentActivity) => {
        set(
          (state) => ({
            agentActivities: [activity, ...state.agentActivities].slice(0, 100), // Keep last 100 activities
          }),
          false,
          'addAgentActivity'
        );
      },

      updateSystemHealth: (health: SystemHealth) => {
        set({ systemHealth: health }, false, 'updateSystemHealth');
      },

      clearSession: () => {
        const newSessionId = uuidv4(); // Use proper UUID format for N8N compatibility
        set({
          sessionId: newSessionId,
          messages: [],
          personalityState: initialPersonalityState,
          sessionState: null,
          agentActivities: [],
          activeAgents: [],
          conversationInsights: null,
        }, false, 'clearSession');
      },

      initializeAgents: () => {
        set({ agents: defaultAgents }, false, 'initializeAgents');
      },

      sendMessage: async (content: string) => {
        const { sessionId, addMessage, setLoading, updatePersonalityState, updateAgentStatus, addAgentActivity } = get();
        
        if (!content.trim()) return;

        const userMessage: Message = {
          id: uuidv4(),
          role: 'user',
          content: content.trim(),
          timestamp: new Date().toISOString(),
        };

        addMessage(userMessage);
        setLoading(true);

        // Update agent statuses to show they're processing
        updateAgentStatus('personality-detector', 'processing');
        updateAgentStatus('behavioral-regulator', 'processing');
        updateAgentStatus('response-generator', 'processing');
        updateAgentStatus('quality-verifier', 'processing');

        try {
          const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';
          const startTime = Date.now();

          const response = await fetch(`${apiUrl}/api/chat/message`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              session_id: sessionId,
              message: content.trim(),
            }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const data = await response.json();
          const processingTime = Date.now() - startTime;

          // Add assistant's response
          const assistantMessage: Message = {
            id: uuidv4(),
            role: 'assistant',
            content: data.message?.content || data.reply || 'I apologize, but I encountered an issue processing your message.',
            timestamp: new Date().toISOString(),
            metadata: {
              processingTime,
              confidence: data.verification?.adherence_score || 0,
              refinementApplied: data.verification?.refinement_applied || false,
              emotionalState: data.personality_state?.emotional_state,
            },
          };

          addMessage(assistantMessage);

          // Update personality state with Phase 1 enhanced data
          if (data.personality_state) {
            updatePersonalityState({
              ocean: data.personality_state.ocean || { O: 0, C: 0, E: 0, A: 0, N: 0 },
              stable: data.personality_state.stable || false,
              confidence_scores: data.personality_state.confidence || {},
              policy_plan: data.regulation?.directives || [],
              ema_applied: data.personality_state.ema_applied || false,
              turn_number: data.turn_index || 0,
            });
          }

          // Log agent activities
          const agentActivities = [
            {
              agentId: 'personality-detector',
              action: 'Personality Detection Completed',
              timestamp: new Date().toISOString(),
              duration: processingTime * 0.3,
              success: true,
              details: {
                ocean_detected: data.personality_state?.ocean,
                ema_applied: data.personality_state?.ema_applied,
                confidence: data.personality_state?.confidence_scores,
              },
            },
            {
              agentId: 'behavioral-regulator',
              action: 'Directive Regulation Completed',
              timestamp: new Date().toISOString(),
              duration: processingTime * 0.2,
              success: true,
              details: {
                directives: data.regulation?.directives,
                analysis: data.regulation?.analysis,
              },
            },
            {
              agentId: 'response-generator',
              action: 'Response Generation Completed',
              timestamp: new Date().toISOString(),
              duration: processingTime * 0.3,
              success: true,
              details: {
                response_length: data.reply?.length,
                model_used: 'gpt-4-therapeutic',
              },
            },
            {
              agentId: 'quality-verifier',
              action: 'Quality Verification Completed',
              timestamp: new Date().toISOString(),
              duration: processingTime * 0.2,
              success: true,
              details: {
                verification_status: data.verification?.status,
                adherence_score: data.verification?.adherence_score,
                refinement_applied: data.verification?.refinement_applied,
              },
            },
          ];

          agentActivities.forEach(addAgentActivity);

          // Update all agents to active status
          ['personality-detector', 'behavioral-regulator', 'response-generator', 'quality-verifier'].forEach(
            (agentId) => updateAgentStatus(agentId, 'active')
          );

          get().setConnectionStatus('connected');
        } catch (error) {
          console.error('Error sending message:', error);
          get().setConnectionStatus('error');

          // Add error message
          const errorMessage: Message = {
            id: uuidv4(),
            role: 'assistant',
            content: 'I apologize, but I\'m having trouble connecting to the personality detection system. Please check if the Phase 1 API server is running.',
            timestamp: new Date().toISOString(),
          };

          addMessage(errorMessage);

          // Update agents to error status
          ['personality-detector', 'behavioral-regulator', 'response-generator', 'quality-verifier'].forEach(
            (agentId) => updateAgentStatus(agentId, 'error')
          );
        } finally {
          setLoading(false);
        }
      },

      fetchSessionHistory: async () => {
        const { sessionId } = get();
        try {
          const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';
          const response = await fetch(`${apiUrl}/api/chat/session/${sessionId}`);
          
          if (response.ok) {
            const sessionData = await response.json();
            set({ sessionState: sessionData }, false, 'fetchSessionHistory');
          }
        } catch (error) {
          console.error('Error fetching session history:', error);
        }
      },
    }),
    {
      name: 'personality-store',
      version: 1,
    }
  )
);
