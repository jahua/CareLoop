'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Bot, 
  Brain, 
  Shield, 
  MessageSquare, 
  Settings2,
  Activity,
  CheckCircle,
  AlertCircle,
  Clock,
  Zap,
  TrendingUp,
  Eye,
  RefreshCw
} from 'lucide-react';
import { usePersonalityStore } from '../store/usePersonalityStore';
import { cn, formatTime } from '../lib/utils';
import { Agent, AgentActivity } from '../types';

interface MultiAgentDashboardProps {
  className?: string;
}

const AgentIcons = {
  detector: Brain,
  regulator: Settings2,
  generator: MessageSquare,
  verifier: Shield,
  coordinator: Bot,
};

const AgentColors = {
  detector: 'text-purple-600 bg-purple-100',
  regulator: 'text-blue-600 bg-blue-100',
  generator: 'text-green-600 bg-green-100',
  verifier: 'text-orange-600 bg-orange-100',
  coordinator: 'text-indigo-600 bg-indigo-100',
};

const StatusColors = {
  active: 'bg-green-500 text-green-50',
  idle: 'bg-gray-400 text-gray-50',
  processing: 'bg-blue-500 text-blue-50',
  error: 'bg-red-500 text-red-50',
};

export default function MultiAgentDashboard({ className }: MultiAgentDashboardProps) {
  const { agents, agentActivities, systemHealth } = usePersonalityStore();
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [showActivities, setShowActivities] = useState(false);

  const getStatusIcon = (status: Agent['status']) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="w-4 h-4" />;
      case 'processing':
        return <RefreshCw className="w-4 h-4 animate-spin" />;
      case 'error':
        return <AlertCircle className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  const getAgentActivities = (agentId: string) => {
    return agentActivities
      .filter(activity => activity.agentId === agentId)
      .slice(0, 5); // Show last 5 activities
  };

  const AgentCard = ({ agent }: { agent: Agent }) => {
    const Icon = AgentIcons[agent.role];
    const isSelected = selectedAgent === agent.id;
    const recentActivities = getAgentActivities(agent.id);

    return (
      <motion.div
        layout
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className={cn(
          "border rounded-lg p-4 cursor-pointer transition-all duration-200",
          isSelected ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:shadow-md',
          agent.status === 'error' ? 'border-red-200' : 'border-gray-200'
        )}
        onClick={() => setSelectedAgent(isSelected ? null : agent.id)}
      >
        {/* Agent Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-3">
            <div className={cn("p-2 rounded-lg", AgentColors[agent.role])}>
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900 text-sm">{agent.name}</h3>
              <p className="text-xs text-gray-500 capitalize">{agent.role}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <div className={cn(
              "flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium",
              StatusColors[agent.status]
            )}>
              {getStatusIcon(agent.status)}
              <span className="capitalize">{agent.status}</span>
            </div>
          </div>
        </div>

        {/* Agent Metrics */}
        <div className="grid grid-cols-3 gap-2 mb-3 text-xs">
          <div className="text-center p-2 bg-gray-50 rounded">
            <div className="font-medium text-gray-900">
              {Math.round(agent.performance.successRate * 100)}%
            </div>
            <div className="text-gray-500">Success</div>
          </div>
          <div className="text-center p-2 bg-gray-50 rounded">
            <div className="font-medium text-gray-900">
              {agent.performance.averageProcessingTime}ms
            </div>
            <div className="text-gray-500">Avg Time</div>
          </div>
          <div className="text-center p-2 bg-gray-50 rounded">
            <div className="font-medium text-gray-900">
              {agent.performance.totalProcessed}
            </div>
            <div className="text-gray-500">Processed</div>
          </div>
        </div>

        {/* Agent Capabilities */}
        <div className="flex flex-wrap gap-1 mb-3">
          {agent.capabilities.slice(0, 2).map((capability, index) => (
            <span
              key={index}
              className="inline-block bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs"
            >
              {capability}
            </span>
          ))}
          {agent.capabilities.length > 2 && (
            <span className="text-xs text-gray-500">
              +{agent.capabilities.length - 2} more
            </span>
          )}
        </div>

        {/* Recent Activity Indicator */}
        {recentActivities.length > 0 && (
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Last activity:</span>
            <span>{formatTime(recentActivities[0].timestamp)}</span>
          </div>
        )}

        {/* Expanded Agent Details */}
        <AnimatePresence>
          {isSelected && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-4 pt-4 border-t border-gray-200"
            >
              {/* Full Capabilities */}
              <div className="mb-3">
                <h4 className="text-xs font-medium text-gray-900 mb-2">All Capabilities</h4>
                <div className="flex flex-wrap gap-1">
                  {agent.capabilities.map((capability, index) => (
                    <span
                      key={index}
                      className="inline-block bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs"
                    >
                      {capability}
                    </span>
                  ))}
                </div>
              </div>

              {/* Recent Activities */}
              {recentActivities.length > 0 && (
                <div>
                  <h4 className="text-xs font-medium text-gray-900 mb-2">Recent Activities</h4>
                  <div className="space-y-2">
                    {recentActivities.map((activity, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between p-2 bg-gray-50 rounded text-xs"
                      >
                        <div className="flex items-center space-x-2">
                          <div className={cn(
                            "w-2 h-2 rounded-full",
                            activity.success ? 'bg-green-500' : 'bg-red-500'
                          )} />
                          <span className="text-gray-900">{activity.action}</span>
                        </div>
                        <div className="flex items-center space-x-2 text-gray-500">
                          {activity.duration && (
                            <span>{activity.duration}ms</span>
                          )}
                          <span>{formatTime(activity.timestamp)}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    );
  };

  return (
    <div className={cn("space-y-4", className)}>
      {/* Dashboard Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Bot className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-gray-900">Multi-Agent System</h2>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowActivities(!showActivities)}
            className={cn(
              "px-3 py-1 text-xs rounded-md border transition-colors",
              showActivities 
                ? 'bg-blue-100 text-blue-700 border-blue-200' 
                : 'bg-gray-100 text-gray-700 border-gray-200'
            )}
          >
            <Activity className="w-3 h-3 mr-1 inline" />
            Activities
          </button>
        </div>
      </div>

      {/* System Health */}
      {systemHealth && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className={cn(
            "p-3 rounded-lg border text-sm",
            systemHealth.status === 'healthy' ? 'bg-green-50 border-green-200 text-green-700' :
            systemHealth.status === 'degraded' ? 'bg-yellow-50 border-yellow-200 text-yellow-700' :
            'bg-red-50 border-red-200 text-red-700'
          )}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="font-medium">System Status:</span>
              <span className="capitalize">{systemHealth.status}</span>
            </div>
            <span className="text-xs opacity-75">
              v{systemHealth.version}
            </span>
          </div>
          <div className="mt-1 text-xs opacity-75">
            API: {systemHealth.services?.api || 'unknown'} | 
            DB: {systemHealth.services?.database || 'unknown'} | 
            N8N: {systemHealth.services?.n8n || 'unknown'}
          </div>
        </motion.div>
      )}

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {agents.map((agent) => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>

      {/* Activity Feed */}
      <AnimatePresence>
        {showActivities && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border rounded-lg p-4"
          >
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-medium text-gray-900">Recent Agent Activities</h3>
              <span className="text-xs text-gray-500">
                Last {Math.min(agentActivities.length, 10)} activities
              </span>
            </div>
            
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {agentActivities.slice(0, 10).map((activity, index) => {
                const agent = agents.find(a => a.id === activity.agentId);
                const Icon = agent ? AgentIcons[agent.role] : Bot;
                
                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="flex items-center space-x-3 p-2 hover:bg-gray-50 rounded"
                  >
                    <div className={cn(
                      "p-1 rounded",
                      agent ? AgentColors[agent.role] : 'text-gray-600 bg-gray-100'
                    )}>
                      <Icon className="w-3 h-3" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-900 truncate">
                          {activity.action}
                        </span>
                        <div className="flex items-center space-x-2 text-xs text-gray-500 ml-2">
                          {activity.duration && (
                            <span>{activity.duration}ms</span>
                          )}
                          <span>{formatTime(activity.timestamp)}</span>
                        </div>
                      </div>
                      
                      {activity.details && (
                        <div className="text-xs text-gray-500 truncate">
                          {typeof activity.details === 'object' 
                            ? Object.keys(activity.details).join(', ')
                            : String(activity.details)
                          }
                        </div>
                      )}
                    </div>
                    
                    <div className={cn(
                      "w-2 h-2 rounded-full flex-shrink-0",
                      activity.success ? 'bg-green-500' : 'bg-red-500'
                    )} />
                  </motion.div>
                );
              })}
              
              {agentActivities.length === 0 && (
                <div className="text-center text-gray-500 py-8">
                  <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No agent activities yet</p>
                  <p className="text-xs">Start a conversation to see agents in action</p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Agent Statistics Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-lg font-semibold text-gray-900">
            {agents.filter(a => a.status === 'active').length}
          </div>
          <div className="text-xs text-gray-600">Active Agents</div>
        </div>
        
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-lg font-semibold text-gray-900">
            {agentActivities.filter(a => a.success).length}
          </div>
          <div className="text-xs text-gray-600">Successful Actions</div>
        </div>
        
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-lg font-semibold text-gray-900">
            {Math.round(
              agents.reduce((sum, agent) => sum + agent.performance.averageProcessingTime, 0) / 
              agents.length
            )}ms
          </div>
          <div className="text-xs text-gray-600">Avg Response Time</div>
        </div>
        
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-lg font-semibold text-gray-900">
            {Math.round(
              agents.reduce((sum, agent) => sum + agent.performance.successRate, 0) / 
              agents.length * 100
            )}%
          </div>
          <div className="text-xs text-gray-600">Overall Success Rate</div>
        </div>
      </div>
    </div>
  );
}
