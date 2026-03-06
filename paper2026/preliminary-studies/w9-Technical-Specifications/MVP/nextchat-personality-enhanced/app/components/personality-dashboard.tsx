/**
 * NextChat-Enhanced: Personality Dashboard Component
 * Integrated with NextChat's UI patterns and styling
 */

import React, { useState, useMemo } from "react";
import styles from "./personality-dashboard.module.scss";
import { 
  usePersonalityStore, 
  PersonalityTrait, 
  PersonalityState, 
  getPersonalityTraitName, 
  getPersonalityTraitDescription 
} from "../store/personality";
import { Modal, List, ListItem } from "./ui-lib";
import { IconButton } from "./button";
import { useMobileScreen } from "../utils";
import Locale from "../locales";

// Icons (using NextChat's icon patterns)
import BrainIcon from "../icons/brain.svg";
import ChartIcon from "../icons/chart.svg";
import InfoIcon from "../icons/info.svg";
import TrendIcon from "../icons/trend.svg";
import SettingsIcon from "../icons/settings.svg";
import LoadingIcon from "../icons/three-dots.svg";
import MaxIcon from "../icons/max.svg";
import MinIcon from "../icons/min.svg";

interface PersonalityDashboardProps {
  className?: string;
  showHeader?: boolean;
  compact?: boolean;
}

interface TraitCardProps {
  trait: PersonalityTrait;
  value: number;
  confidence: number;
  rawValue?: number;
  emaApplied?: boolean;
  onClick?: () => void;
}

const TRAIT_INFO = {
  O: {
    name: 'Openness',
    emoji: '🎨',
    color: '#8B5CF6', // Purple
    description: 'Creativity, curiosity, willingness to try new things',
    low: 'Practical, conventional, prefers routine',
    high: 'Creative, curious, open to new experiences'
  },
  C: {
    name: 'Conscientiousness',
    emoji: '📋',
    color: '#3B82F6', // Blue
    description: 'Organization, discipline, goal-directed behavior',
    low: 'Flexible, spontaneous, relaxed approach',
    high: 'Organized, disciplined, detail-oriented'
  },
  E: {
    name: 'Extraversion',
    emoji: '🗣️',
    color: '#10B981', // Green
    description: 'Social energy, assertiveness, positive emotions',
    low: 'Quiet, reserved, prefers smaller groups',
    high: 'Outgoing, energetic, socially confident'
  },
  A: {
    name: 'Agreeableness',
    emoji: '🤝',
    color: '#F59E0B', // Yellow
    description: 'Cooperation, trust, empathy for others',
    low: 'Direct, competitive, skeptical',
    high: 'Cooperative, trusting, empathetic'
  },
  N: {
    name: 'Neuroticism',
    emoji: '💭',
    color: '#EF4444', // Red
    description: 'Emotional stability, stress resilience',
    low: 'Calm, stable, stress-resilient',
    high: 'Sensitive, emotionally reactive'
  }
};

const TraitCard: React.FC<TraitCardProps> = ({ 
  trait, 
  value, 
  confidence, 
  rawValue, 
  emaApplied, 
  onClick 
}) => {
  const info = TRAIT_INFO[trait];
  const normalizedValue = ((value + 1) / 2) * 100; // Convert from [-1,1] to [0,100]
  const confidencePercent = Math.round(confidence * 100);
  
  const getValueColor = () => {
    if (confidence < 0.3) return '#9CA3AF'; // Gray for low confidence
    return value > 0 ? info.color : `${info.color}80`; // Semi-transparent for negative
  };

  const getInterpretation = () => {
    if (confidence < 0.3) return 'Insufficient data';
    return value > 0.3 ? info.high : value < -0.3 ? info.low : 'Moderate level';
  };

  return (
    <div className={styles["trait-card"]} onClick={onClick}>
      <div className={styles["trait-header"]}>
        <div className={styles["trait-icon"]}>
          <span style={{ fontSize: '20px' }}>{info.emoji}</span>
        </div>
        <div className={styles["trait-info"]}>
          <h4 className={styles["trait-name"]}>{info.name}</h4>
          <span className={styles["trait-label"]}>{trait} Trait</span>
        </div>
        <div className={styles["trait-value"]}>
          <span className={styles["value"]} style={{ color: getValueColor() }}>
            {value.toFixed(2)}
          </span>
          <span className={styles["confidence"]}>
            {confidencePercent}% conf
          </span>
        </div>
      </div>
      
      <div className={styles["trait-progress"]}>
        <div className={styles["progress-bar"]}>
          <div 
            className={styles["progress-fill"]}
            style={{ 
              width: `${normalizedValue}%`,
              backgroundColor: getValueColor(),
            }}
          />
          <div className={styles["progress-center"]} />
        </div>
      </div>
      
      <div className={styles["trait-interpretation"]}>
        {getInterpretation()}
      </div>
      
      {emaApplied && rawValue !== undefined && (
        <div className={styles["ema-indicator"]}>
          <span>🔄 EMA: Raw {rawValue.toFixed(2)} → Smoothed {value.toFixed(2)}</span>
        </div>
      )}
    </div>
  );
};

export function PersonalityDashboard({ 
  className, 
  showHeader = true,
  compact = false 
}: PersonalityDashboardProps) {
  const isMobile = useMobileScreen();
  const [selectedTrait, setSelectedTrait] = useState<PersonalityTrait | null>(null);
  const [showInsights, setShowInsights] = useState(false);
  
  const {
    personalityState,
    agents,
    systemHealth,
    isPersonalityEnabled,
    conversationInsights,
    enablePersonality,
    updatePersonalityState,
  } = usePersonalityStore();

  const overallConfidence = useMemo(() => {
    const scores = Object.values(personalityState.confidence_scores);
    return scores.reduce((sum, score) => sum + score, 0) / scores.length;
  }, [personalityState.confidence_scores]);

  const strongTraits = useMemo(() => {
    return Object.entries(personalityState.ocean)
      .filter(([_, value]) => Math.abs(value) > 0.3)
      .length;
  }, [personalityState.ocean]);

  const personalityAgents = useMemo(() => {
    return agents.filter(agent => 
      agent.personalityFocus === 'OCEAN' || 
      agent.personalityFocus === 'therapeutic'
    );
  }, [agents]);

  if (!isPersonalityEnabled) {
    return (
      <div className={`${styles["personality-disabled"]} ${className}`}>
        <div className={styles["disabled-content"]}>
          <BrainIcon />
          <h3>Personality Detection Disabled</h3>
          <p>Enable personality detection to see OCEAN trait analysis and therapeutic adaptation.</p>
          <IconButton
            onClick={() => enablePersonality(true)}
            text="Enable Personality"
            icon={<SettingsIcon />}
          />
        </div>
      </div>
    );
  }

  return (
    <div className={`${styles["personality-dashboard"]} ${className}`}>
      {showHeader && (
        <div className={styles["dashboard-header"]}>
          <div className={styles["header-left"]}>
            <BrainIcon />
            <div>
              <h2>Personality Profile</h2>
              <span className={styles["subtitle"]}>OCEAN Trait Analysis</span>
            </div>
          </div>
          <div className={styles["header-right"]}>
            <div className={`${styles["status-badge"]} ${personalityState.stable ? styles["stable"] : styles["learning"]}`}>
              {personalityState.stable ? '🎯 Stable' : '🔄 Learning'}
            </div>
            <IconButton
              onClick={() => setShowInsights(true)}
              icon={<InfoIcon />}
              title="View Insights"
            />
          </div>
        </div>
      )}

      {/* Overview Cards */}
      {!compact && (
        <div className={styles["overview-cards"]}>
          <div className={styles["overview-card"]}>
            <div className={styles["card-value"]}>{Math.round(overallConfidence * 100)}%</div>
            <div className={styles["card-label"]}>Overall Confidence</div>
          </div>
          <div className={styles["overview-card"]}>
            <div className={styles["card-value"]}>{strongTraits}/5</div>
            <div className={styles["card-label"]}>Strong Traits</div>
          </div>
          <div className={styles["overview-card"]}>
            <div className={styles["card-value"]}>{personalityState.turn_number}</div>
            <div className={styles["card-label"]}>Conversation Turns</div>
          </div>
          <div className={styles["overview-card"]}>
            <div className={styles["card-value"]}>
              {personalityState.verification_stats.average_adherence 
                ? Math.round(personalityState.verification_stats.average_adherence * 100) + '%'
                : '--'
              }
            </div>
            <div className={styles["card-label"]}>Response Quality</div>
          </div>
        </div>
      )}

      {/* OCEAN Traits */}
      <div className={styles["traits-section"]}>
        <div className={styles["section-header"]}>
          <h3>OCEAN Personality Traits</h3>
          {personalityState.ema_applied && (
            <span className={styles["ema-badge"]}>EMA Smoothing Active</span>
          )}
        </div>
        
        <div className={styles["traits-grid"]}>
          {Object.entries(personalityState.ocean).map(([trait, value]) => (
            <TraitCard
              key={trait}
              trait={trait as PersonalityTrait}
              value={value}
              confidence={personalityState.confidence_scores[trait as PersonalityTrait]}
              rawValue={personalityState.ocean_raw?.[trait as PersonalityTrait]}
              emaApplied={personalityState.ema_applied}
              onClick={() => setSelectedTrait(trait as PersonalityTrait)}
            />
          ))}
        </div>
      </div>

      {/* Current Adaptation Strategy */}
      {personalityState.policy_plan.length > 0 && (
        <div className={styles["adaptation-section"]}>
          <h3>Current Adaptation Strategy</h3>
          <div className={styles["policy-list"]}>
            {personalityState.policy_plan.map((policy, index) => (
              <div key={index} className={styles["policy-item"]}>
                <span className={styles["policy-number"]}>{index + 1}</span>
                <span className={styles["policy-text"]}>{policy}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Agent Status (if not compact) */}
      {!compact && personalityAgents.length > 0 && (
        <div className={styles["agents-section"]}>
          <h3>Personality Agents</h3>
          <div className={styles["agents-list"]}>
            {personalityAgents.map((agent) => (
              <div key={agent.id} className={styles["agent-card"]}>
                <div className={styles["agent-info"]}>
                  <span className={styles["agent-name"]}>{agent.name}</span>
                  <span className={styles["agent-role"]}>{agent.role}</span>
                </div>
                <div className={`${styles["agent-status"]} ${styles[agent.status]}`}>
                  {agent.status}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Detection Progress */}
      {!personalityState.stable && (
        <div className={styles["progress-section"]}>
          <h3>Personality Detection Progress</h3>
          <div className={styles["progress-info"]}>
            <span>{personalityState.turn_number} / {personalityState.stabilization_turns} turns</span>
            <span>{Math.round(overallConfidence * 100)}% confidence</span>
          </div>
          <div className={styles["progress-bar-large"]}>
            <div 
              className={styles["progress-fill-large"]}
              style={{ 
                width: `${Math.min((personalityState.turn_number / personalityState.stabilization_turns) * 100, 100)}%`
              }}
            />
          </div>
          <p className={styles["progress-tip"]}>
            💭 Keep chatting! The AI needs more conversation to accurately detect your personality traits.
          </p>
        </div>
      )}

      {/* System Health Indicator */}
      {systemHealth && (
        <div className={`${styles["health-section"]} ${styles[systemHealth.status]}`}>
          <div className={styles["health-info"]}>
            <span>System: {systemHealth.status}</span>
            <span>API: {systemHealth.services.api}</span>
            <span>DB: {systemHealth.services.database}</span>
          </div>
        </div>
      )}

      {/* Trait Detail Modal */}
      {selectedTrait && (
        <Modal
          title={`${TRAIT_INFO[selectedTrait].emoji} ${TRAIT_INFO[selectedTrait].name}`}
          onClose={() => setSelectedTrait(null)}
          actions={[
            <IconButton
              key="close"
              onClick={() => setSelectedTrait(null)}
              text="Close"
              type="primary"
            />
          ]}
        >
          <div className={styles["trait-detail"]}>
            <div className={styles["trait-description"]}>
              <p>{TRAIT_INFO[selectedTrait].description}</p>
            </div>
            
            <div className={styles["trait-interpretations"]}>
              <div className={styles["interpretation-card"]}>
                <h4>High {TRAIT_INFO[selectedTrait].name}</h4>
                <p>{TRAIT_INFO[selectedTrait].high}</p>
              </div>
              <div className={styles["interpretation-card"]}>
                <h4>Low {TRAIT_INFO[selectedTrait].name}</h4>
                <p>{TRAIT_INFO[selectedTrait].low}</p>
              </div>
            </div>

            <div className={styles["trait-stats"]}>
              <div className={styles["stat-item"]}>
                <span>Current Value:</span>
                <span>{personalityState.ocean[selectedTrait].toFixed(2)}</span>
              </div>
              <div className={styles["stat-item"]}>
                <span>Confidence:</span>
                <span>{Math.round(personalityState.confidence_scores[selectedTrait] * 100)}%</span>
              </div>
              {personalityState.ocean_raw && (
                <div className={styles["stat-item"]}>
                  <span>Raw Detection:</span>
                  <span>{personalityState.ocean_raw[selectedTrait].toFixed(2)}</span>
                </div>
              )}
            </div>
          </div>
        </Modal>
      )}

      {/* Insights Modal */}
      {showInsights && conversationInsights && (
        <Modal
          title="🔍 Conversation Insights"
          onClose={() => setShowInsights(false)}
          actions={[
            <IconButton
              key="close"
              onClick={() => setShowInsights(false)}
              text="Close"
              type="primary"
            />
          ]}
        >
          <div className={styles["insights-content"]}>
            {/* Implementation of insights visualization */}
            <div className={styles["insight-section"]}>
              <h4>Personality Evolution</h4>
              <p>Track how your personality traits have evolved over the conversation.</p>
              {/* Add charts/visualizations here */}
            </div>
            
            <div className={styles["insight-section"]}>
              <h4>Therapeutic Progress</h4>
              <p>Analysis of therapeutic adaptation and progress indicators.</p>
              <List>
                {conversationInsights.therapeuticProgress.directivesUsed.map((directive, index) => (
                  <ListItem key={index} title={directive} />
                ))}
              </List>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
}

// Compact version for sidebar integration
export function PersonalityWidget({ className }: { className?: string }) {
  return (
    <PersonalityDashboard 
      className={className}
      showHeader={false}
      compact={true}
    />
  );
}

















































