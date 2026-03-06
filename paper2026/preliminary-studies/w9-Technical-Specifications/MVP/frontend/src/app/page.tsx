'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Toaster } from 'react-hot-toast';
import { 
  Layout, 
  Settings, 
  Brain, 
  Bot,
  Activity,
  BarChart3,
  Zap
} from 'lucide-react';
import { usePersonalityStore } from '../store/usePersonalityStore';
import EnhancedChatInterface from '../components/EnhancedChatInterface';
import EnhancedPersonalityDashboard from '../components/EnhancedPersonalityDashboard';
import MultiAgentDashboard from '../components/MultiAgentDashboard';
import ClientOnly from '../components/ClientOnly';
import { cn } from '../lib/utils';

type ViewMode = 'chat' | 'personality' | 'agents' | 'analytics';

export default function Home() {
  const {
    sessionId,
    messages,
    personalityState,
    connectionStatus,
    systemHealth,
    clearSession,
    initializeAgents,
    fetchSessionHistory,
  } = usePersonalityStore();

  const [viewMode, setViewMode] = useState<ViewMode>('chat');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Initialize on mount
  useEffect(() => {
    // Generate session ID on client side to avoid hydration mismatch
    if (!sessionId) {
      // Use crypto.randomUUID() for proper UUID format (N8N compatible)
      const newSessionId = crypto.randomUUID();
      usePersonalityStore.getState().setSessionId(newSessionId);
    }
    
    initializeAgents();
    
    // Test API connection
    const testConnection = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';
        const response = await fetch(`${apiUrl}/api/health`);
        if (response.ok) {
          const health = await response.json();
          usePersonalityStore.getState().updateSystemHealth(health);
          usePersonalityStore.getState().setConnectionStatus('connected');
        }
      } catch (error) {
        console.warn('API connection test failed:', error);
        usePersonalityStore.getState().setConnectionStatus('error');
      }
    };

    testConnection();
    
    // Fetch session history if available
    if (sessionId) {
      fetchSessionHistory();
    }
  }, [sessionId, initializeAgents, fetchSessionHistory]);

  const navigationItems = [
    { id: 'chat', label: 'Chat', icon: Brain, color: 'text-blue-600' },
    { id: 'personality', label: 'Personality', icon: BarChart3, color: 'text-purple-600' },
    { id: 'agents', label: 'Multi-Agent', icon: Bot, color: 'text-green-600' },
  ];

  const renderMainContent = () => {
    switch (viewMode) {
      case 'personality':
        return <EnhancedPersonalityDashboard className="h-full" />;
      case 'agents':
        return <MultiAgentDashboard className="h-full" />;
      default:
        return (
          <div className="grid grid-cols-1 xl:grid-cols-4 gap-6 h-full">
            {/* Chat Interface */}
            <div className="xl:col-span-2 flex flex-col">
              <EnhancedChatInterface className="flex-1" />
            </div>
            
            {/* Side Panels */}
            <div className="xl:col-span-2 space-y-6 overflow-y-auto">
              {/* Personality Panel */}
              <div className="min-h-[400px]">
                <EnhancedPersonalityDashboard />
              </div>
              
              {/* Agent Panel */}
              {!sidebarCollapsed && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="min-h-[300px]"
                >
                  <MultiAgentDashboard />
                </motion.div>
              )}
            </div>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />

      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white border-b border-gray-200 px-6 py-4"
      >
        <div className="flex items-center justify-between">
          {/* Logo & Title */}
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                Personality AI
              </h1>
              <p className="text-sm text-gray-500">
                Phase 1 Enhanced Multi-Agent System
              </p>
            </div>
          </div>

          {/* Navigation */}
          <div className="hidden md:flex items-center space-x-1 bg-gray-100 rounded-lg p-1">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setViewMode(item.id as ViewMode)}
                  className={cn(
                    "flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-all",
                    viewMode === item.id
                      ? 'bg-white shadow-sm text-gray-900'
                      : 'text-gray-600 hover:text-gray-900'
                  )}
                >
                  <Icon className={cn("w-4 h-4", viewMode === item.id ? item.color : '')} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>

          {/* Status & Actions */}
          <div className="flex items-center space-x-4">
            {/* Connection Status */}
            <div className={cn(
              "flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-medium",
              connectionStatus === 'connected' ? 'bg-green-100' :
              connectionStatus === 'error' ? 'bg-red-100' :
              'bg-yellow-100'
            )}
            style={{
              color: connectionStatus === 'connected' ? '#047857' :
                     connectionStatus === 'error' ? '#B91C1C' :
                     '#B45309'
            }}>
              <div className={cn(
                "w-2 h-2 rounded-full",
                connectionStatus === 'connected' ? 'bg-green-500' :
                connectionStatus === 'error' ? 'bg-red-500' :
                'bg-yellow-500'
              )} />
              <span style={{
                color: connectionStatus === 'connected' ? '#047857' :
                       connectionStatus === 'error' ? '#B91C1C' :
                       '#B45309'
              }}>
                {connectionStatus === 'connected' ? 'Connected' :
                 connectionStatus === 'error' ? 'Disconnected' :
                 'Connecting...'}
              </span>
            </div>

            {/* Session Info */}
            <div className="hidden lg:block text-xs font-medium" style={{ color: '#6B7280' }}>
              Session: {sessionId ? sessionId.slice(0, 8) + '...' : 'Loading...'}
            </div>

            {/* Clear Session */}
            <button
              onClick={clearSession}
              className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
              title="Clear Session"
            >
              Clear
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden mt-4">
          <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => setViewMode(item.id as ViewMode)}
                  className={cn(
                    "flex-1 flex items-center justify-center space-x-1 py-2 rounded-md text-xs font-medium transition-all",
                    viewMode === item.id
                      ? 'bg-white shadow-sm text-gray-900'
                      : 'text-gray-600'
                  )}
                >
                  <Icon className={cn("w-3 h-3", viewMode === item.id ? item.color : '')} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </motion.header>

      {/* System Health Alert */}
      <AnimatePresence>
        {systemHealth && systemHealth.status !== 'healthy' && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className={cn(
              "px-6 py-3 text-sm",
              systemHealth.status === 'degraded' ? 'bg-yellow-50 text-yellow-700 border-b border-yellow-200' :
              'bg-red-50 text-red-700 border-b border-red-200'
            )}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Zap className="w-4 h-4" />
                <span>
                  System Status: {systemHealth.status === 'degraded' ? 'Some services degraded' : 'System issues detected'}
                </span>
              </div>
              <span className="text-xs opacity-75">
                Check: API ({systemHealth.services.api}), DB ({systemHealth.services.database}), N8N ({systemHealth.services.n8n})
              </span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <main className="p-6 h-[calc(100vh-80px)]">
        <motion.div
          key={viewMode}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
          className="h-full"
        >
          {renderMainContent()}
        </motion.div>
      </main>

      {/* Floating Quick Stats */}
      <ClientOnly fallback={
        <div className="fixed bottom-6 right-6 bg-white rounded-lg shadow-lg border p-3 text-xs space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Loading...</span>
          </div>
        </div>
      }>
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="fixed bottom-6 right-6 bg-white rounded-lg shadow-lg border p-3 text-xs space-y-1"
        >
          <div className="flex items-center justify-between">
            <span className="text-gray-600">Messages:</span>
            <span className="font-medium">{messages.length}</span>
          </div>
          <div className="flex items-center justify-between">
            <span style={{ color: '#4B5563' }}>Personality:</span>
            <span className="font-medium" style={{
              color: personalityState.stable ? '#059669' : '#2563EB'
            }}>
              {personalityState.stable ? 'Stable' : 'Learning'}
            </span>
          </div>
          {personalityState.ema_applied && (
            <div className="flex items-center justify-between">
              <span className="text-gray-600">EMA:</span>
              <span className="font-medium text-purple-600">Active</span>
            </div>
          )}
        </motion.div>
      </ClientOnly>
    </div>
  );
}

















