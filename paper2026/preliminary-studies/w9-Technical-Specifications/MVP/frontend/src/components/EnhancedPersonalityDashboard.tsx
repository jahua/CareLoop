'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, 
  TrendingUp, 
  Target, 
  Zap, 
  Eye,
  BarChart3,
  Info,
  ChevronDown,
  ChevronUp,
  Activity
} from 'lucide-react';
import { LineChart, Line, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';
import { usePersonalityStore } from '../store/usePersonalityStore';
import { cn, getPersonalityColor, getConfidenceText, normalizePersonalityValue } from '../lib/utils';
import { PersonalityState } from '../types';

interface EnhancedPersonalityDashboardProps {
  className?: string;
}

const TRAIT_INFO = {
  O: {
    name: 'Openness',
    description: 'Creativity, curiosity, willingness to try new things',
    low: 'Practical, conventional, prefers routine',
    high: 'Creative, curious, open to new experiences',
    icon: '🎨',
    color: 'purple',
  },
  C: {
    name: 'Conscientiousness', 
    description: 'Organization, discipline, goal-directed behavior',
    low: 'Flexible, spontaneous, relaxed approach',
    high: 'Organized, disciplined, detail-oriented',
    icon: '📋',
    color: 'blue',
  },
  E: {
    name: 'Extraversion',
    description: 'Social energy, assertiveness, positive emotions',
    low: 'Quiet, reserved, prefers smaller groups',
    high: 'Outgoing, energetic, socially confident',
    icon: '🗣️',
    color: 'green',
  },
  A: {
    name: 'Agreeableness',
    description: 'Cooperation, trust, empathy for others',
    low: 'Direct, competitive, skeptical',
    high: 'Cooperative, trusting, empathetic',
    icon: '🤝',
    color: 'yellow',
  },
  N: {
    name: 'Neuroticism',
    description: 'Emotional stability, stress resilience',
    low: 'Calm, stable, stress-resilient',
    high: 'Sensitive, emotionally reactive',
    icon: '💭',
    color: 'red',
  }
};

export default function EnhancedPersonalityDashboard({ className }: EnhancedPersonalityDashboardProps) {
  const { personalityState, messages } = usePersonalityStore();
  const [expandedTrait, setExpandedTrait] = useState<string | null>(null);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const getTraitInterpretation = (trait: keyof typeof TRAIT_INFO, value: number, confidence: number) => {
    if (confidence < 0.3) return 'Insufficient data';
    
    const info = TRAIT_INFO[trait];
    if (value > 0.3) return info.high;
    if (value < -0.3) return info.low;
    return 'Moderate level';
  };

  const getTraitColorClass = (trait: string, value: number, confidence: number) => {
    if (confidence < 0.6) return 'bg-gray-200 text-gray-600';
    
    const colorMap = {
      'purple': value > 0 ? 'bg-purple-500 text-white' : 'bg-purple-200 text-purple-800',
      'blue': value > 0 ? 'bg-blue-500 text-white' : 'bg-blue-200 text-blue-800',
      'green': value > 0 ? 'bg-green-500 text-white' : 'bg-green-200 text-green-800',
      'yellow': value > 0 ? 'bg-yellow-500 text-white' : 'bg-yellow-200 text-yellow-800',
      'red': value > 0 ? 'bg-red-200 text-red-800' : 'bg-red-500 text-white', // Inverted for neuroticism
    };
    
    return colorMap[TRAIT_INFO[trait as keyof typeof TRAIT_INFO].color as keyof typeof colorMap];
  };

  // Prepare radar chart data
  const radarData = Object.entries(personalityState.ocean).map(([trait, value]) => ({
    trait: TRAIT_INFO[trait as keyof typeof TRAIT_INFO].name,
    value: normalizePersonalityValue(value),
    confidence: personalityState.confidence_scores[trait as keyof typeof personalityState.confidence_scores] * 100,
  }));

  // Calculate overall personality metrics
  const averageConfidence = Object.values(personalityState.confidence_scores).reduce((a, b) => a + b, 0) / 5;
  const strongTraits = Object.entries(personalityState.ocean).filter(([_, value]) => Math.abs(value) > 0.3);
  const overallStability = personalityState.stable ? 1 : averageConfidence;

  const TraitCard = ({ trait, value }: { trait: keyof typeof TRAIT_INFO; value: number }) => {
    const confidence = personalityState.confidence_scores[trait];
    const info = TRAIT_INFO[trait];
    const isExpanded = expandedTrait === trait;
    const normalizedValue = normalizePersonalityValue(value);

    return (
      <motion.div
        layout
        className={cn(
          "border rounded-lg p-4 cursor-pointer transition-all duration-200",
          isExpanded ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:shadow-md'
        )}
        onClick={() => setExpandedTrait(isExpanded ? null : trait)}
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <span className="text-lg">{info.icon}</span>
            <div>
              <h3 className="font-medium text-gray-900">{info.name}</h3>
              <p className="text-xs text-gray-500">{trait} Trait</p>
            </div>
          </div>
          
          <div className="text-right">
            <div className={cn(
              "text-sm font-medium px-2 py-1 rounded",
              getTraitColorClass(trait, value, confidence)
            )}>
              {value.toFixed(2)}
            </div>
            <div className="text-xs text-gray-500 mt-1">
              {getConfidenceText(confidence)}
            </div>
          </div>
        </div>

        {/* Progress bar */}
        <div className="relative mb-3">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <motion.div
              className={getTraitColorClass(trait, value, confidence).replace('text-white', '').replace('text-gray-600', '').replace('text-purple-800', '').replace('text-blue-800', '').replace('text-green-800', '').replace('text-yellow-800', '').replace('text-red-800', '')}
              initial={{ width: 0 }}
              animate={{ width: `${normalizedValue}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
              style={{ height: '8px' }}
            />
          </div>
          <div className="absolute top-0 left-1/2 w-0.5 h-2 bg-gray-400" />
        </div>

        {/* Basic interpretation */}
        <p className="text-xs text-gray-600 mb-2">
          {getTraitInterpretation(trait, value, confidence)}
        </p>

        {/* EMA indicator */}
        {personalityState.ema_applied && personalityState.ocean_raw && (
          <div className="flex items-center justify-between text-xs">
            <span className="text-blue-600">🔄 EMA Smoothed</span>
            <span className="text-gray-500">
              Raw: {personalityState.ocean_raw[trait].toFixed(2)}
            </span>
          </div>
        )}

        <div className="flex items-center justify-center mt-2">
          {isExpanded ? (
            <ChevronUp className="w-4 h-4 text-gray-400" />
          ) : (
            <ChevronDown className="w-4 h-4 text-gray-400" />
          )}
        </div>

        {/* Expanded details */}
        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mt-4 pt-4 border-t border-gray-200"
            >
              <div className="space-y-3">
                {/* Detailed description */}
                <div>
                  <h4 className="text-xs font-medium text-gray-900 mb-1">Description</h4>
                  <p className="text-xs text-gray-600">{info.description}</p>
                </div>

                {/* High/Low interpretations */}
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="p-2 bg-green-50 rounded">
                    <div className="font-medium text-green-800 mb-1">High {info.name}</div>
                    <div className="text-green-700">{info.high}</div>
                  </div>
                  <div className="p-2 bg-orange-50 rounded">
                    <div className="font-medium text-orange-800 mb-1">Low {info.name}</div>
                    <div className="text-orange-700">{info.low}</div>
                  </div>
                </div>

                {/* Confidence breakdown */}
                <div>
                  <h4 className="text-xs font-medium text-gray-900 mb-1">Detection Confidence</h4>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-1">
                      <div
                        className="bg-blue-500 h-1 rounded-full transition-all duration-300"
                        style={{ width: `${confidence * 100}%` }}
                      />
                    </div>
                    <span className="text-xs font-medium text-gray-700">
                      {Math.round(confidence * 100)}%
                    </span>
                  </div>
                </div>

                {/* EMA details */}
                {personalityState.ema_applied && (
                  <div className="p-2 bg-blue-50 rounded">
                    <div className="text-xs font-medium text-blue-900 mb-1">EMA Smoothing Details</div>
                    <div className="text-xs text-blue-700 space-y-1">
                      {personalityState.ocean_raw && (
                        <div>Raw Detection: {personalityState.ocean_raw[trait].toFixed(2)}</div>
                      )}
                      <div>Smoothed Value: {value.toFixed(2)}</div>
                      {personalityState.ema_alpha && (
                        <div>Alpha: {personalityState.ema_alpha}</div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    );
  };

  return (
    <div className={cn("space-y-6", className)}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Brain className="w-5 h-5 text-blue-600" />
          <h2 className="text-lg font-semibold text-gray-900">Personality Profile</h2>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className={cn(
            "px-2 py-1 rounded-full text-xs font-medium",
            personalityState.stable 
              ? 'bg-green-100 text-green-800' 
              : 'bg-blue-100 text-blue-800'
          )}>
            {personalityState.stable ? '🎯 Stable' : '🔄 Learning'}
          </div>
          
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
          >
            {showAdvanced ? 'Simple' : 'Advanced'}
          </button>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center p-3 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg"
        >
          <div className="text-lg font-semibold text-blue-900">
            {Math.round(averageConfidence * 100)}%
          </div>
          <div className="text-xs text-blue-700">Overall Confidence</div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-center p-3 bg-gradient-to-br from-green-50 to-green-100 rounded-lg"
        >
          <div className="text-lg font-semibold text-green-900">
            {strongTraits.length}/5
          </div>
          <div className="text-xs text-green-700">Strong Traits</div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-center p-3 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg"
        >
          <div className="text-lg font-semibold text-purple-900">
            {personalityState.turn_number || messages.length}
          </div>
          <div className="text-xs text-purple-700">Conversation Turns</div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-center p-3 bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg"
        >
          <div className="text-lg font-semibold text-orange-900">
            {Math.round(overallStability * 100)}%
          </div>
          <div className="text-xs text-orange-700">Stability Score</div>
        </motion.div>
      </div>

      {/* Advanced View Toggle */}
      <AnimatePresence>
        {showAdvanced && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
          >
            {/* Radar Chart */}
            <div className="bg-white rounded-lg border p-4">
              <h3 className="font-medium text-gray-900 mb-3 flex items-center">
                <BarChart3 className="w-4 h-4 mr-2" />
                Personality Radar
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="trait" className="text-xs" />
                    <PolarRadiusAxis domain={[0, 100]} className="text-xs" />
                    <Radar
                      name="Personality"
                      dataKey="value"
                      stroke="#3b82f6"
                      fill="#3b82f6"
                      fillOpacity={0.3}
                    />
                    <Radar
                      name="Confidence"
                      dataKey="confidence"
                      stroke="#10b981"
                      fill="transparent"
                      strokeDasharray="5 5"
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
              <div className="flex justify-center space-x-4 text-xs mt-2">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-blue-500 rounded mr-1 opacity-30"></div>
                  <span>Personality</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-1 bg-green-500 mr-1"></div>
                  <span>Confidence</span>
                </div>
              </div>
            </div>

            {/* EMA Information */}
            <div className="bg-white rounded-lg border p-4">
              <h3 className="font-medium text-gray-900 mb-3 flex items-center">
                <Zap className="w-4 h-4 mr-2" />
                EMA Smoothing Status
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">EMA Applied:</span>
                  <span className={cn(
                    "px-2 py-1 rounded text-xs font-medium",
                    personalityState.ema_applied ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                  )}>
                    {personalityState.ema_applied ? 'Yes' : 'No'}
                  </span>
                </div>
                
                {personalityState.ema_alpha && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Alpha (Learning Rate):</span>
                    <span className="text-sm font-medium text-gray-900">
                      {personalityState.ema_alpha}
                    </span>
                  </div>
                )}
                
                {personalityState.stabilization_turns && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Stability Threshold:</span>
                    <span className="text-sm font-medium text-gray-900">
                      {personalityState.stabilization_turns} turns
                    </span>
                  </div>
                )}

                <div className="p-3 bg-blue-50 rounded-lg">
                  <div className="text-xs font-medium text-blue-900 mb-1">
                    How EMA Smoothing Works
                  </div>
                  <div className="text-xs text-blue-700">
                    EMA (Exponential Moving Average) gradually adjusts personality estimates over time, 
                    preventing sudden jumps and creating a more stable, reliable personality profile.
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Personality Traits Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(personalityState.ocean).map(([trait, value]) => (
          <TraitCard
            key={trait}
            trait={trait as keyof typeof TRAIT_INFO}
            value={value}
          />
        ))}
      </div>

      {/* Current Adaptation Strategy */}
      {personalityState.policy_plan.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg border p-4"
        >
          <h3 className="font-medium text-gray-900 mb-3 flex items-center">
            <Target className="w-4 h-4 mr-2" />
            Current Adaptation Strategy
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {personalityState.policy_plan.map((policy, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-start space-x-2 p-3 bg-blue-50 rounded-md border border-blue-100"
              >
                <div className="flex-shrink-0 w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
                  {index + 1}
                </div>
                <span className="text-sm text-blue-800 leading-relaxed">
                  {policy}
                </span>
              </motion.div>
            ))}
          </div>
          
          <div className="mt-3 text-xs text-gray-600 flex items-center">
            <Info className="w-3 h-3 mr-1" />
            The AI uses these behavioral guidelines to adapt its communication style to your personality.
          </div>
        </motion.div>
      )}

      {/* Detection Progress */}
      {!personalityState.stable && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border p-4"
        >
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-medium text-gray-900 flex items-center">
              <Activity className="w-4 h-4 mr-2" />
              Personality Detection Progress
            </h3>
            <span className="text-xs text-gray-500">
              {personalityState.turn_number || messages.length} / {personalityState.stabilization_turns || 5} turns
            </span>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
            <motion.div
              className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ 
                width: `${Math.min(((personalityState.turn_number || messages.length) / (personalityState.stabilization_turns || 5)) * 100, 100)}%` 
              }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            />
          </div>
          
          <div className="text-xs text-gray-600">
            💭 Keep chatting! The AI needs more conversation to accurately detect and stabilize your personality traits.
          </div>
        </motion.div>
      )}
    </div>
  );
}
