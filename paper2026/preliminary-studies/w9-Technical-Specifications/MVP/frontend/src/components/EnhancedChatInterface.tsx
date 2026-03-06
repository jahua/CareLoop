'use client';

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Brain, 
  MessageSquare, 
  Zap, 
  CheckCircle, 
  AlertTriangle,
  MoreVertical,
  Copy,
  RefreshCw,
  Settings
} from 'lucide-react';
import { usePersonalityStore } from '../store/usePersonalityStore';
import { cn, formatTime } from '../lib/utils';
import { Message } from '../types';

interface EnhancedChatInterfaceProps {
  className?: string;
}

export default function EnhancedChatInterface({ className }: EnhancedChatInterfaceProps) {
  const {
    messages,
    personalityState,
    isLoading,
    connectionStatus,
    sendMessage,
  } = usePersonalityStore();

  const [inputValue, setInputValue] = useState('');
  const [showActions, setShowActions] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Auto-resize textarea
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }, [inputValue]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !isLoading) {
      await sendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const copyMessage = (content: string) => {
    navigator.clipboard.writeText(content);
    setShowActions(null);
  };

  const getMessageIcon = (message: Message) => {
    if (message.role === 'user') return null;
    
    if (message.metadata?.refinementApplied) {
      return <RefreshCw className="w-4 h-4 text-orange-500" />;
    }
    
    if (message.metadata?.confidence && message.metadata.confidence > 0.8) {
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    }
    
    return <Brain className="w-4 h-4 text-blue-500" />;
  };

  const getMessageMetadata = (message: Message) => {
    if (!message.metadata) return null;
    
    return (
      <div className="flex items-center space-x-2 text-xs text-gray-500 mt-1">
        {message.metadata.processingTime && (
          <span>⚡ {message.metadata.processingTime}ms</span>
        )}
        {message.metadata.confidence && (
          <span>🎯 {Math.round(message.metadata.confidence * 100)}%</span>
        )}
        {message.metadata.refinementApplied && (
          <span className="text-orange-600">🔧 Refined</span>
        )}
        {message.metadata.emotionalState && (
          <span className="text-purple-600">😊 {message.metadata.emotionalState}</span>
        )}
      </div>
    );
  };

  return (
    <div className={cn("flex flex-col h-full bg-white rounded-lg shadow-sm border", className)}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-blue-50 to-purple-50">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2">
            <Brain className="w-6 h-6 text-blue-600" />
            <h2 className="text-lg font-semibold text-gray-800">
              Personality-Adaptive Chat
            </h2>
          </div>
          
          {/* Connection Status */}
          <div className={cn(
            "flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium",
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
        </div>

        {/* Personality Status */}
        <div className="flex items-center space-x-2">
          {personalityState.policy_plan.length > 0 && (
            <div className="text-xs bg-white px-2 py-1 rounded-md border" style={{ color: '#4B5563' }}>
              <span className="font-medium">{personalityState.policy_plan.length}</span> active policies
            </div>
          )}
          
          <div className={cn(
            "px-2 py-1 rounded-full text-xs font-medium",
            personalityState.stable 
              ? 'bg-green-100' 
              : 'bg-blue-100'
          )}
          style={{
            color: personalityState.stable ? '#166534' : '#1E40AF'
          }}>
            {personalityState.stable ? '🎯 Stable' : '🔄 Learning'}
          </div>
        </div>
      </div>

      {/* Current Policy Display */}
      {personalityState.policy_plan.length > 0 && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="px-4 py-2 bg-blue-50 border-b"
        >
          <div className="text-xs font-medium mb-1" style={{ color: '#1E3A8A' }}>Current Adaptation Strategy:</div>
          <div className="flex flex-wrap gap-1">
            {personalityState.policy_plan.slice(0, 3).map((policy, index) => (
              <span
                key={index}
                className="inline-block bg-blue-100 px-2 py-1 rounded-md text-xs"
                style={{ color: '#1E40AF' }}
              >
                {policy}
              </span>
            ))}
            {personalityState.policy_plan.length > 3 && (
              <span className="text-xs" style={{ color: '#2563EB' }}>
                +{personalityState.policy_plan.length - 3} more
              </span>
            )}
          </div>
        </motion.div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: "spring", bounce: 0.5 }}
            >
              <div className="text-6xl mb-4">🧠💬</div>
              <h3 className="text-lg font-medium mb-2">Welcome to Personality-Adaptive AI</h3>
              <p className="text-sm max-w-md mx-auto leading-relaxed">
                Start a conversation and watch as the AI learns about your personality traits 
                and adapts its communication style in real-time using advanced EMA smoothing 
                and multi-agent coordination.
              </p>
              <div className="mt-4 text-xs text-gray-400">
                💡 Try sharing your thoughts, feelings, or asking questions
              </div>
            </motion.div>
          </div>
        ) : (
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className={cn(
                  "flex",
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                )}
              >
                <div
                  className={cn(
                    "max-w-[80%] rounded-lg p-3 relative group",
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-800 border'
                  )}
                  onMouseEnter={() => setShowActions(message.id)}
                  onMouseLeave={() => setShowActions(null)}
                >
                  {/* Message Content */}
                  <div className="flex items-start space-x-2">
                    {message.role === 'assistant' && (
                      <div className="flex-shrink-0 mt-1">
                        {getMessageIcon(message)}
                      </div>
                    )}
                    <div className="flex-1">
                      <div className="text-sm leading-relaxed whitespace-pre-wrap">
                        {message.content}
                      </div>
                      
                      {/* Metadata */}
                      {getMessageMetadata(message)}
                      
                      {/* Timestamp */}
                      <div className={cn(
                        "text-xs mt-2 opacity-70",
                        message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                      )}>
                        {formatTime(message.timestamp)}
                      </div>
                    </div>
                  </div>

                  {/* Message Actions */}
                  <AnimatePresence>
                    {showActions === message.id && (
                      <motion.div
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.8 }}
                        className={cn(
                          "absolute top-2 right-2 flex items-center space-x-1",
                          message.role === 'user' ? 'text-blue-200' : 'text-gray-500'
                        )}
                      >
                        <button
                          onClick={() => copyMessage(message.content)}
                          className="p-1 hover:bg-black/10 rounded"
                          title="Copy message"
                        >
                          <Copy className="w-3 h-3" />
                        </button>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        )}

        {/* Typing indicator */}
        <AnimatePresence>
          {isLoading && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="flex justify-start"
            >
              <div className="bg-gray-100 rounded-lg p-3 border flex items-center space-x-2">
                <div className="flex space-x-1">
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0 }}
                    className="w-2 h-2 bg-gray-400 rounded-full"
                  />
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }}
                    className="w-2 h-2 bg-gray-400 rounded-full"
                  />
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }}
                    className="w-2 h-2 bg-gray-400 rounded-full"
                  />
                </div>
                <span className="text-xs text-gray-600">
                  AI agents are processing...
                </span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-gray-50">
        <form onSubmit={handleSubmit} className="flex items-end space-x-2">
          <div className="flex-1">
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={
                personalityState.stable 
                  ? "The AI has adapted to your personality - type your message..."
                  : "Type your message... (AI is learning your personality traits)"
              }
              className={cn(
                "w-full px-3 py-2 border rounded-lg resize-none min-h-[44px] max-h-[120px]",
                "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                "disabled:opacity-50 disabled:cursor-not-allowed",
                "transition-all duration-200",
                "bg-white text-gray-900"
              )}
              disabled={isLoading || connectionStatus === 'error'}
              rows={1}
            />
          </div>
          
          <motion.button
            type="submit"
            disabled={!inputValue.trim() || isLoading || connectionStatus === 'error'}
            className={cn(
              "px-4 py-2 bg-blue-600 text-white rounded-lg",
              "hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
              "disabled:opacity-50 disabled:cursor-not-allowed transition-colors",
              "flex items-center space-x-1"
            )}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {isLoading ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              >
                <Zap className="w-4 h-4" />
              </motion.div>
            ) : (
              <Send className="w-4 h-4" />
            )}
          </motion.button>
        </form>
        
        {/* Helpful tips */}
        {messages.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mt-3 text-xs text-gray-500 text-center"
          >
            💡 The more you share about your thoughts and feelings, the better the AI can adapt
          </motion.div>
        )}

        {/* EMA Information */}
        {personalityState.ema_applied && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-2 text-xs text-blue-600 text-center"
          >
            🔄 EMA smoothing is active - personality changes are being applied gradually
          </motion.div>
        )}
      </div>
    </div>
  );
}
