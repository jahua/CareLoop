'use client';

import { useState, useEffect, useRef } from 'react';
import ChatInterface from '../components/ChatInterface';
import PersonalityDashboard from '../components/PersonalityDashboard';
import { v4 as uuidv4 } from 'uuid';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface PersonalityState {
  ocean: {
    O: number; // Openness
    C: number; // Conscientiousness
    E: number; // Extraversion
    A: number; // Agreeableness
    N: number; // Neuroticism
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
}

export default function Home() {
  const [sessionId] = useState(() => uuidv4());
  const [messages, setMessages] = useState<Message[]>([]);
  const [personalityState, setPersonalityState] = useState<PersonalityState>({
    ocean: { O: 0, C: 0, E: 0, A: 0, N: 0 },
    stable: false,
    confidence_scores: { O: 0, C: 0, E: 0, A: 0, N: 0 },
    policy_plan: []
  });
  const [isLoading, setIsLoading] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'error'>('connecting');

  // Test connection on mount
  useEffect(() => {
    const testConnection = async () => {
      try {
        const webhookUrl = process.env.NEXT_PUBLIC_N8N_WEBHOOK_URL || 'http://localhost:5678/webhook';
        const response = await fetch(`${webhookUrl}/test`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (response.ok || response.status === 404) {
          // 404 is expected if the test endpoint doesn't exist, but N8N is running
          setConnectionStatus('connected');
        } else {
          setConnectionStatus('error');
        }
      } catch (error) {
        console.warn('N8N connection test failed:', error);
        setConnectionStatus('error');
      }
    };

    testConnection();
  }, []);

  const sendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const webhookUrl = process.env.NEXT_PUBLIC_N8N_WEBHOOK_URL || 'http://localhost:5678/webhook';
      const response = await fetch(`${webhookUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: content.trim()
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Add assistant's response
      const assistantMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: data.reply || 'I apologize, but I encountered an issue processing your message.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Update personality state
      if (data.ocean_preview) {
        setPersonalityState({
          ocean: data.ocean_preview,
          stable: data.personality_stable || false,
          confidence_scores: data.confidence_scores || { O: 0, C: 0, E: 0, A: 0, N: 0 },
          policy_plan: data.policy_plan || []
        });
      }

      setConnectionStatus('connected');
    } catch (error) {
      console.error('Error sending message:', error);
      setConnectionStatus('error');
      
      // Add error message
      const errorMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: 'I apologize, but I\'m having trouble connecting to the personality detection system. Please check if N8N is running and try again.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearSession = () => {
    setMessages([]);
    setPersonalityState({
      ocean: { O: 0, C: 0, E: 0, A: 0, N: 0 },
      stable: false,
      confidence_scores: { O: 0, C: 0, E: 0, A: 0, N: 0 },
      policy_plan: []
    });
  };

  return (
    <div className="space-y-6">
      {/* Connection Status */}
      <div className={`p-3 rounded-md text-sm ${
        connectionStatus === 'connected' ? 'bg-green-50 text-green-700 border border-green-200' :
        connectionStatus === 'error' ? 'bg-red-50 text-red-700 border border-red-200' :
        'bg-yellow-50 text-yellow-700 border border-yellow-200'
      }`}>
        Status: {
          connectionStatus === 'connected' ? '✅ Connected to N8N workflow system' :
          connectionStatus === 'error' ? '❌ Connection failed - Check if N8N is running on port 5678' :
          '🔄 Testing connection...'
        }
      </div>

      {/* Session Info */}
      <div className="bg-white rounded-lg shadow-sm border p-4">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-lg font-semibold text-gray-800">Chat Session</h2>
          <button
            onClick={clearSession}
            className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            disabled={isLoading}
          >
            Clear Session
          </button>
        </div>
        <p className="text-sm text-gray-600">
          Session ID: <code className="bg-gray-100 px-2 py-1 rounded text-xs">{sessionId}</code>
        </p>
        <p className="text-sm text-gray-600 mt-1">
          Messages: {messages.length} | Personality Stable: {personalityState.stable ? '✅ Yes' : '⏳ Detecting...'}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chat Interface */}
        <div className="lg:col-span-2">
          <ChatInterface
            messages={messages}
            onSendMessage={sendMessage}
            isLoading={isLoading}
            personalityState={personalityState}
          />
        </div>

        {/* Personality Dashboard */}
        <div className="lg:col-span-1">
          <PersonalityDashboard personalityState={personalityState} />
        </div>
      </div>
    </div>
  );
}
















