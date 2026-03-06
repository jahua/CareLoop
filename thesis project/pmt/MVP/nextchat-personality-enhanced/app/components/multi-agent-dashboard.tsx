/**
 * NextChat-Enhanced: Multi-Agent Dashboard Component
 * Real-time agent monitoring integrated with NextChat's UI patterns
 */

import React, { useState, useMemo, useCallback } from "react";
import styles from "./multi-agent-dashboard.module.scss";
import { usePersonalityStore, Agent, AgentActivity } from "../store/personality";
import { Modal, List, ListItem } from "./ui-lib";
import { IconButton } from "./button";
import { useMobileScreen } from "../utils";
import { showToast } from "./ui-lib";
import Locale from "../locales";

// Icons following NextChat patterns
import BotIcon from "../icons/bot.svg";
import BrainIcon from "../icons/brain.svg";
import SettingsIcon from "../icons/settings.svg";
import LoadingIcon from "../icons/three-dots.svg";
import ActivityIcon from "../icons/lightning.svg";
import SuccessIcon from "../icons/confirm.svg";
import ErrorIcon from "../icons/close.svg";
import InfoIcon from "../icons/info.svg";
import MaxIcon from "../icons/max.svg";
import MinIcon from "../icons/min.svg";
import ResetIcon from "../icons/reload.svg";

interface MultiAgentDashboardProps {
  className?: string;
  showHeader?: boolean;
  compact?: boolean;
}

interface AgentCardProps {
  agent: Agent;
  activities: AgentActivity[];
  onAgentClick?: (agent: Agent) => void;
  compact?: boolean;
}

const AGENT_ICONS = {
  detector: BrainIcon,
  regulator: SettingsIcon,
  generator: BotIcon,
  verifier: SuccessIcon,
  coordinator: ActivityIcon,
};

const AGENT_COLORS = {
  detector: '#8B5CF6', // Purple
  regulator: '#3B82F6', // Blue  
  generator: '#10B981', // Green
  verifier: '#F59E0B', // Amber
  coordinator: '#6366F1', // Indigo
};

const STATUS_COLORS = {
  active: '#10B981',    // Green
  idle: '#9CA3AF',      // Gray
  processing: '#3B82F6', // Blue
  error: '#EF4444',     // Red
};

const AgentCard: React.FC<AgentCardProps> = ({ 
  agent, 
  activities, 
  onAgentClick, 
  compact = false 
}) => {
  const [showDetails, setShowDetails] = useState(false);
  const Icon = AGENT_ICONS[agent.role];
  const agentColor = AGENT_COLORS[agent.role];
  const statusColor = STATUS_COLORS[agent.status];
  
  const recentActivities = useMemo(() => 
    activities.filter(a => a.agentId === agent.id).slice(0, 3),
    [activities, agent.id]
  );

  const successRate = agent.performance.successRate * 100;
  const avgTime = agent.performance.averageProcessingTime;

  return (
    <div 
      className={`${styles["agent-card"]} ${compact ? styles["compact"] : ""}`}
      onClick={() => onAgentClick?.(agent)}
    >
      {/* Agent Header */}
      <div className={styles["agent-header"]}>
        <div className={styles["agent-icon"]} style={{ backgroundColor: `${agentColor}20` }}>
          <Icon style={{ fill: agentColor }} />
        </div>
        <div className={styles["agent-info"]}>
          <h4 className={styles["agent-name"]}>{agent.name}</h4>
          <span className={styles["agent-role"]}>{agent.role}</span>
        </div>
        <div 
          className={`${styles["agent-status"]} ${styles[agent.status]}`}
          style={{ backgroundColor: `${statusColor}20`, color: statusColor }}
        >
          <div 
            className={styles["status-dot"]} 
            style={{ backgroundColor: statusColor }}
          />
          {agent.status}
          {agent.status === 'processing' && (
            <LoadingIcon className={styles["loading-icon"]} />
          )}
        </div>
      </div>

      {/* Agent Metrics */}
      {!compact && (
        <div className={styles["agent-metrics"]}>
          <div className={styles["metric"]}>
            <span className={styles["metric-value"]}>{Math.round(successRate)}%</span>
            <span className={styles["metric-label"]}>Success</span>
          </div>
          <div className={styles["metric"]}>
            <span className={styles["metric-value"]}>{avgTime}ms</span>
            <span className={styles["metric-label"]}>Avg Time</span>
          </div>
          <div className={styles["metric"]}>
            <span className={styles["metric-value"]}>{agent.performance.totalProcessed}</span>
            <span className={styles["metric-label"]}>Processed</span>
          </div>
        </div>
      )}

      {/* Agent Capabilities */}
      {!compact && (
        <div className={styles["agent-capabilities"]}>
          {agent.capabilities.slice(0, 2).map((capability, index) => (
            <span key={index} className={styles["capability-tag"]}>
              {capability}
            </span>
          ))}
          {agent.capabilities.length > 2 && (
            <span className={styles["capability-more"]}>
              +{agent.capabilities.length - 2} more
            </span>
          )}
        </div>
      )}

      {/* Recent Activity */}
      {!compact && recentActivities.length > 0 && (
        <div className={styles["recent-activity"]}>
          <div className={styles["activity-header"]}>
            <span>Recent Activity</span>
            <span className={styles["activity-time"]}>
              {new Date(recentActivities[0].timestamp).toLocaleTimeString([], { 
                hour: '2-digit', 
                minute: '2-digit' 
              })}
            </span>
          </div>
          <div className={styles["activity-list"]}>
            {recentActivities.map((activity, index) => (
              <div key={index} className={styles["activity-item"]}>
                <div 
                  className={`${styles["activity-status"]} ${activity.success ? styles["success"] : styles["error"]}`}
                />
                <span className={styles["activity-text"]}>
                  {activity.action}
                </span>
                {activity.duration && (
                  <span className={styles["activity-duration"]}>
                    {activity.duration}ms
                  </span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Expand/Collapse for compact mode */}
      {compact && (
        <div className={styles["agent-summary"]}>
          <span>{Math.round(successRate)}% success</span>
          <span>{agent.performance.totalProcessed} processed</span>
        </div>
      )}
    </div>
  );
};

export function MultiAgentDashboard({ 
  className, 
  showHeader = true, 
  compact = false 
}: MultiAgentDashboardProps) {
  const isMobile = useMobileScreen();
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [showActivities, setShowActivities] = useState(false);
  const [showSystemConfig, setShowSystemConfig] = useState(false);
  
  const {
    agents,
    agentActivities,
    systemHealth,
    updateAgentStatus,
    addAgentActivity,
  } = usePersonalityStore();

  const systemStats = useMemo(() => {
    const activeAgents = agents.filter(a => a.status === 'active').length;
    const successfulActions = agentActivities.filter(a => a.success).length;
    const totalActions = agentActivities.length;
    const avgResponseTime = agents.reduce((sum, agent) => sum + agent.performance.averageProcessingTime, 0) / agents.length;
    const overallSuccessRate = agents.reduce((sum, agent) => sum + agent.performance.successRate, 0) / agents.length * 100;

    return {
      activeAgents,
      successfulActions,
      totalActions,
      avgResponseTime: Math.round(avgResponseTime),
      overallSuccessRate: Math.round(overallSuccessRate),
    };
  }, [agents, agentActivities]);

  const handleAgentClick = useCallback((agent: Agent) => {
    setSelectedAgent(agent);
  }, []);

  const handleResetAgent = useCallback((agentId: string) => {
    updateAgentStatus(agentId, 'idle');
    showToast(`Agent ${agentId} reset to idle state`);
  }, [updateAgentStatus]);

  return (
    <div className={`${styles["multi-agent-dashboard"]} ${className}`}>
      {showHeader && (
        <div className={styles["dashboard-header"]}>
          <div className={styles["header-left"]}>
            <ActivityIcon />
            <div>
              <h2>Multi-Agent System</h2>
              <span className={styles["subtitle"]}>Phase 1 Enhanced Pipeline</span>
            </div>
          </div>
          <div className={styles["header-right"]}>
            <div className={styles["system-status"]}>
              {systemHealth && (
                <div className={`${styles["health-indicator"]} ${styles[systemHealth.status]}`}>
                  {systemHealth.status}
                </div>
              )}
            </div>
            <IconButton
              onClick={() => setShowActivities(!showActivities)}
              icon={<InfoIcon />}
              title="Show Activities"
              className={showActivities ? styles["active"] : ""}
            />
            <IconButton
              onClick={() => setShowSystemConfig(true)}
              icon={<SettingsIcon />}
              title="System Configuration"
            />
          </div>
        </div>
      )}

      {/* System Overview */}
      {!compact && (
        <div className={styles["system-overview"]}>
          <div className={styles["overview-card"]}>
            <div className={styles["card-value"]}>{systemStats.activeAgents}</div>
            <div className={styles["card-label"]}>Active Agents</div>
          </div>
          <div className={styles["overview-card"]}>
            <div className={styles["card-value"]}>{systemStats.successfulActions}</div>
            <div className={styles["card-label"]}>Successful Actions</div>
          </div>
          <div className={styles["overview-card"]}>
            <div className={styles["card-value"]}>{systemStats.avgResponseTime}ms</div>
            <div className={styles["card-label"]}>Avg Response Time</div>
          </div>
          <div className={styles["overview-card"]}>
            <div className={styles["card-value"]}>{systemStats.overallSuccessRate}%</div>
            <div className={styles["card-label"]}>Success Rate</div>
          </div>
        </div>
      )}

      {/* Agents Grid */}
      <div className={styles["agents-section"]}>
        <div className={styles["section-header"]}>
          <h3>Pipeline Agents</h3>
          <span className={styles["agent-count"]}>
            {agents.length} agents • {systemStats.activeAgents} active
          </span>
        </div>
        
        <div className={`${styles["agents-grid"]} ${compact ? styles["compact"] : ""}`}>
          {agents.map((agent) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              activities={agentActivities}
              onAgentClick={handleAgentClick}
              compact={compact}
            />
          ))}
        </div>
      </div>

      {/* Activity Feed */}
      {showActivities && !compact && (
        <div className={styles["activity-section"]}>
          <div className={styles["section-header"]}>
            <h3>Recent Agent Activities</h3>
            <span className={styles["activity-count"]}>
              Last {Math.min(agentActivities.length, 10)} activities
            </span>
          </div>
          
          <div className={styles["activity-feed"]}>
            {agentActivities.slice(0, 10).map((activity, index) => {
              const agent = agents.find(a => a.id === activity.agentId);
              const Icon = agent ? AGENT_ICONS[agent.role] : BotIcon;
              const agentColor = agent ? AGENT_COLORS[agent.role] : '#9CA3AF';
              
              return (
                <div key={index} className={styles["activity-item"]}>
                  <div 
                    className={styles["activity-icon"]}
                    style={{ backgroundColor: `${agentColor}20` }}
                  >
                    <Icon style={{ fill: agentColor }} />
                  </div>
                  
                  <div className={styles["activity-content"]}>
                    <div className={styles["activity-header"]}>
                      <span className={styles["activity-text"]}>
                        {activity.action}
                      </span>
                      <div className={styles["activity-meta"]}>
                        {activity.duration && (
                          <span>{activity.duration}ms</span>
                        )}
                        <span>
                          {new Date(activity.timestamp).toLocaleTimeString([], { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                          })}
                        </span>
                      </div>
                    </div>
                    
                    {activity.details && (
                      <div className={styles["activity-details"]}>
                        {typeof activity.details === 'object' 
                          ? Object.keys(activity.details).slice(0, 3).join(', ')
                          : String(activity.details)
                        }
                      </div>
                    )}
                  </div>
                  
                  <div 
                    className={`${styles["activity-status"]} ${activity.success ? styles["success"] : styles["error"]}`}
                  />
                </div>
              );
            })}
            
            {agentActivities.length === 0 && (
              <div className={styles["no-activities"]}>
                <ActivityIcon />
                <p>No agent activities yet</p>
                <span>Start a conversation to see agents in action</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Agent Detail Modal */}
      {selectedAgent && (
        <Modal
          title={`${selectedAgent.name} Details`}
          onClose={() => setSelectedAgent(null)}
          actions={[
            <IconButton
              key="reset"
              onClick={() => handleResetAgent(selectedAgent.id)}
              text="Reset"
              icon={<ResetIcon />}
              type="primary"
            />,
            <IconButton
              key="close"
              onClick={() => setSelectedAgent(null)}
              text="Close"
            />
          ]}
        >
          <div className={styles["agent-detail"]}>
            <div className={styles["agent-detail-header"]}>
              <div className={styles["detail-icon"]}>
                {React.createElement(AGENT_ICONS[selectedAgent.role], {
                  style: { fill: AGENT_COLORS[selectedAgent.role] }
                })}
              </div>
              <div>
                <h3>{selectedAgent.name}</h3>
                <p>Role: {selectedAgent.role} • Focus: {selectedAgent.personalityFocus}</p>
                <p>Model: {selectedAgent.model}</p>
              </div>
            </div>

            <div className={styles["detail-section"]}>
              <h4>Performance Metrics</h4>
              <div className={styles["metrics-grid"]}>
                <div className={styles["metric-card"]}>
                  <span className={styles["metric-label"]}>Success Rate</span>
                  <span className={styles["metric-value"]}>
                    {Math.round(selectedAgent.performance.successRate * 100)}%
                  </span>
                </div>
                <div className={styles["metric-card"]}>
                  <span className={styles["metric-label"]}>Avg Processing Time</span>
                  <span className={styles["metric-value"]}>
                    {selectedAgent.performance.averageProcessingTime}ms
                  </span>
                </div>
                <div className={styles["metric-card"]}>
                  <span className={styles["metric-label"]}>Total Processed</span>
                  <span className={styles["metric-value"]}>
                    {selectedAgent.performance.totalProcessed}
                  </span>
                </div>
              </div>
            </div>

            <div className={styles["detail-section"]}>
              <h4>Capabilities</h4>
              <div className={styles["capabilities-list"]}>
                {selectedAgent.capabilities.map((capability, index) => (
                  <div key={index} className={styles["capability-item"]}>
                    {capability}
                  </div>
                ))}
              </div>
            </div>

            <div className={styles["detail-section"]}>
              <h4>Recent Activities</h4>
              <List>
                {agentActivities
                  .filter(a => a.agentId === selectedAgent.id)
                  .slice(0, 5)
                  .map((activity, index) => (
                    <ListItem
                      key={index}
                      title={activity.action}
                      subTitle={`${activity.success ? '✅' : '❌'} ${new Date(activity.timestamp).toLocaleString()}`}
                    />
                  ))
                }
              </List>
            </div>
          </div>
        </Modal>
      )}

      {/* System Configuration Modal */}
      {showSystemConfig && (
        <Modal
          title="⚙️ Multi-Agent System Configuration"
          onClose={() => setShowSystemConfig(false)}
          actions={[
            <IconButton
              key="close"
              onClick={() => setShowSystemConfig(false)}
              text="Close"
              type="primary"
            />
          ]}
        >
          <div className={styles["config-content"]}>
            <div className={styles["config-section"]}>
              <h4>System Health</h4>
              {systemHealth ? (
                <div className={styles["health-details"]}>
                  <div className={styles["health-item"]}>
                    <span>Status:</span>
                    <span className={`${styles["health-value"]} ${styles[systemHealth.status]}`}>
                      {systemHealth.status}
                    </span>
                  </div>
                  <div className={styles["health-item"]}>
                    <span>API:</span>
                    <span>{systemHealth.services.api}</span>
                  </div>
                  <div className={styles["health-item"]}>
                    <span>Database:</span>
                    <span>{systemHealth.services.database}</span>
                  </div>
                  <div className={styles["health-item"]}>
                    <span>N8N:</span>
                    <span>{systemHealth.services.n8n}</span>
                  </div>
                </div>
              ) : (
                <p>System health data not available</p>
              )}
            </div>

            <div className={styles["config-section"]}>
              <h4>Agent Pipeline</h4>
              <p>The Phase 1 enhanced pipeline consists of 5 specialized agents working together:</p>
              <ol>
                <li>Personality Detection Agent - OCEAN trait analysis with EMA smoothing</li>
                <li>Behavioral Regulation Agent - Therapeutic directive mapping</li>
                <li>Response Generation Agent - Personality-adapted response creation</li>
                <li>Quality Verification Agent - Response quality assessment and refinement</li>
                <li>Session Coordination Agent - Multi-agent orchestration and crisis detection</li>
              </ol>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}

// Compact version for sidebar integration
export function MultiAgentWidget({ className }: { className?: string }) {
  return (
    <MultiAgentDashboard 
      className={className}
      showHeader={false}
      compact={true}
    />
  );
}

















































