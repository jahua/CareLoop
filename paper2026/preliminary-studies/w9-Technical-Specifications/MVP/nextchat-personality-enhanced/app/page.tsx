/**
 * NextChat-Enhanced: Main Page
 * Entry point combining NextChat UI with Phase 1 personality features
 */

"use client";

import { useEffect, useState } from "react";
import { nanoid } from "nanoid";
import { usePersonalityStore } from "./store/personality";
import { PersonalityDashboard } from "./components/personality-dashboard";
import { MultiAgentDashboard } from "./components/multi-agent-dashboard";

// NextChat-style loading component
function Loading() {
  return (
    <div className="loading-container">
      <div className="loading-content">
        <div className="loading-spinner" />
        <h2>NextChat-Enhanced</h2>
        <p>Initializing personality-adaptive AI system...</p>
      </div>
    </div>
  );
}

// Simple chat interface for demonstration
function SimpleChatInterface() {
  const [messages, setMessages] = useState<Array<{
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: string;
    personality_data?: any;
  }>>([]);
  
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => `session-${Date.now()}-${nanoid()}`);
  
  const {
    personalityState,
    agents,
    systemHealth,
    isPersonalityEnabled,
    updateSystemHealth,
    checkSystemHealth,
  } = usePersonalityStore();

  // Initialize system health check
  useEffect(() => {
    const initializeSystem = async () => {
      try {
        const health = await checkSystemHealth();
        updateSystemHealth(health);
      } catch (error) {
        console.warn('System health check failed:', error);
      }
    };
    
    initializeSystem();
  }, [checkSystemHealth, updateSystemHealth]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;
    
    const userMessage = {
      id: nanoid(),
      role: 'user' as const,
      content: inputValue,
      timestamp: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    
    try {
      // Send to Phase 1 personality detection API
      const response = await fetch('/api/personality', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: inputValue,
          enable_ema: true,
          enable_verification: true,
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        
        const assistantMessage = {
          id: nanoid(),
          role: 'assistant' as const,
          content: data.content || data.fallback_response || "I'm here to help. How are you feeling?",
          timestamp: new Date().toISOString(),
          personality_data: {
            personality_state: data.personality_state,
            verification: data.verification,
            agents_involved: data.agents_involved,
            processing_time: data.processing_time,
          },
        };
        
        setMessages(prev => [...prev, assistantMessage]);
        
        // Update personality state if available
        if (data.personality_state) {
          usePersonalityStore.getState().updatePersonalityState(data.personality_state);
        }
      } else {
        // Fallback response
        const errorData = await response.json().catch(() => ({}));
        const fallbackMessage = {
          id: nanoid(),
          role: 'assistant' as const,
          content: errorData.fallback_response || "I apologize, but I'm experiencing technical difficulties. How can I help you today?",
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, fallbackMessage]);
      }
    } catch (error) {
      console.error('Message send failed:', error);
      const errorMessage = {
        id: nanoid(),
        role: 'assistant' as const,
        content: "I'm sorry, I'm having trouble connecting to the personality detection system. Let me try to help you anyway - what's on your mind?",
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const getSystemStatusColor = () => {
    if (!systemHealth) return '#9CA3AF';
    return systemHealth.status === 'healthy' ? '#10B981' : 
           systemHealth.status === 'degraded' ? '#F59E0B' : '#EF4444';
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="header-left">
          <h1>NextChat-Enhanced</h1>
          <span className="version">v2.16.1-personality</span>
        </div>
        <div className="header-right">
          <div 
            className="system-status" 
            style={{ backgroundColor: getSystemStatusColor() }}
            title={`System Status: ${systemHealth?.status || 'Unknown'}`}
          >
            {systemHealth?.status || '?'}
          </div>
          <span className="session-id">Session: {sessionId.slice(0, 8)}...</span>
        </div>
      </div>
      
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h2>🧠 Welcome to NextChat-Enhanced!</h2>
            <p>This is NextChat enhanced with Phase 1 multi-agent personality detection.</p>
            <div className="features">
              <div className="feature">🎯 OCEAN trait analysis with EMA smoothing</div>
              <div className="feature">🤖 Multi-agent coordination (5 specialized agents)</div>
              <div className="feature">✅ Quality verification and automatic refinement</div>
              <div className="feature">📊 Real-time personality insights and analytics</div>
            </div>
            <p>Start chatting to see personality detection in action!</p>
          </div>
        )}
        
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.role}`}>
            <div className="message-header">
              <span className="role">{message.role === 'user' ? '👤' : '🤖'}</span>
              <span className="timestamp">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
              {message.personality_data && (
                <span className="personality-indicator" title="Personality data available">
                  🧠
                </span>
              )}
            </div>
            <div className="message-content">{message.content}</div>
            
            {message.personality_data && (
              <div className="personality-metadata">
                <span>Agents: {message.personality_data.agents_involved?.join(', ')}</span>
                <span>Time: {message.personality_data.processing_time}</span>
                {message.personality_data.verification && (
                  <span>Quality: {Math.round(message.personality_data.verification.adherence_score * 100)}%</span>
                )}
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant loading">
            <div className="message-header">
              <span className="role">🤖</span>
              <span className="timestamp">Processing...</span>
            </div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>
      
      <div className="chat-input">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Share your thoughts and feelings..."
          disabled={isLoading}
        />
        <button 
          onClick={handleSendMessage}
          disabled={isLoading || !inputValue.trim()}
        >
          {isLoading ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  );
}

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'chat' | 'personality' | 'agents'>('chat');
  
  const { isPersonalityEnabled } = usePersonalityStore();

  useEffect(() => {
    // Simulate initialization
    const timer = setTimeout(() => setIsLoading(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="nextchat-enhanced">
      <nav className="main-nav">
        <button 
          className={activeTab === 'chat' ? 'active' : ''}
          onClick={() => setActiveTab('chat')}
        >
          💬 Chat
        </button>
        <button 
          className={activeTab === 'personality' ? 'active' : ''}
          onClick={() => setActiveTab('personality')}
          disabled={!isPersonalityEnabled}
        >
          🧠 Personality
        </button>
        <button 
          className={activeTab === 'agents' ? 'active' : ''}
          onClick={() => setActiveTab('agents')}
          disabled={!isPersonalityEnabled}
        >
          🤖 Agents
        </button>
      </nav>
      
      <main className="main-content">
        {activeTab === 'chat' && <SimpleChatInterface />}
        {activeTab === 'personality' && <PersonalityDashboard />}
        {activeTab === 'agents' && <MultiAgentDashboard />}
      </main>
      
      {!isPersonalityEnabled && (
        <div className="personality-disabled-notice">
          ⚠️ Personality detection is disabled. Enable it to access advanced features.
        </div>
      )}
    </div>
  );
}

















































