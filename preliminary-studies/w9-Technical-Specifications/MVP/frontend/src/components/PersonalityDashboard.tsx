'use client';

interface PersonalityState {
  ocean: {
    O: number;
    C: number;
    E: number;
    A: number;
    N: number;
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

interface PersonalityDashboardProps {
  personalityState: PersonalityState;
}

const TRAIT_INFO = {
  O: {
    name: 'Openness',
    description: 'Creativity, curiosity, willingness to try new things',
    low: 'Practical, conventional, prefers routine',
    high: 'Creative, curious, open to new experiences'
  },
  C: {
    name: 'Conscientiousness', 
    description: 'Organization, discipline, goal-directed behavior',
    low: 'Flexible, spontaneous, relaxed approach',
    high: 'Organized, disciplined, detail-oriented'
  },
  E: {
    name: 'Extraversion',
    description: 'Social energy, assertiveness, positive emotions',
    low: 'Quiet, reserved, prefers smaller groups',
    high: 'Outgoing, energetic, socially confident'
  },
  A: {
    name: 'Agreeableness',
    description: 'Cooperation, trust, empathy for others',
    low: 'Direct, competitive, skeptical',
    high: 'Cooperative, trusting, empathetic'
  },
  N: {
    name: 'Neuroticism',
    description: 'Emotional stability, stress resilience',
    low: 'Calm, stable, stress-resilient',
    high: 'Sensitive, emotionally reactive'
  }
};

export default function PersonalityDashboard({ personalityState }: PersonalityDashboardProps) {
  const getTraitColor = (value: number, confidence: number) => {
    if (confidence < 0.3) return 'bg-gray-200';
    
    if (value > 0.3) return 'bg-blue-500';
    if (value < -0.3) return 'bg-orange-500';
    return 'bg-gray-400';
  };

  const getTraitTextColor = (value: number, confidence: number) => {
    if (confidence < 0.3) return 'text-gray-600';
    
    if (value > 0.3) return 'text-blue-700';
    if (value < -0.3) return 'text-orange-700';
    return 'text-gray-700';
  };

  const getTraitInterpretation = (trait: keyof typeof TRAIT_INFO, value: number, confidence: number) => {
    if (confidence < 0.3) return 'Insufficient data';
    
    const info = TRAIT_INFO[trait];
    if (value > 0.3) return info.high;
    if (value < -0.3) return info.low;
    return 'Moderate level';
  };

  const normalizeValue = (value: number) => {
    // Convert from [-1, 1] to [0, 100] for display
    return ((value + 1) / 2) * 100;
  };

  return (
    <div className="space-y-4">
      {/* Personality Overview */}
      <div className="bg-white rounded-lg shadow-sm border p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-gray-800">Personality Profile</h3>
          <div className={`px-2 py-1 rounded-full text-xs font-medium ${
            personalityState.stable 
              ? 'bg-green-100 text-green-800' 
              : 'bg-yellow-100 text-yellow-800'
          }`}>
            {personalityState.stable ? 'Stable' : 'Detecting'}
          </div>
        </div>

        {/* OCEAN Traits */}
        <div className="space-y-3">
          {Object.entries(personalityState.ocean).map(([trait, value]) => {
            const confidence = personalityState.confidence_scores[trait as keyof typeof personalityState.confidence_scores];
            const normalizedValue = normalizeValue(value);
            
            return (
              <div key={trait} className="space-y-1">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-700">
                    {TRAIT_INFO[trait as keyof typeof TRAIT_INFO].name}
                  </span>
                  <div className="flex items-center space-x-2">
                    <span className={`text-xs font-medium ${getTraitTextColor(value, confidence)}`}>
                      {value.toFixed(2)}
                    </span>
                    <span className="text-xs text-gray-500">
                      ({Math.round(confidence * 100)}% conf)
                    </span>
                  </div>
                </div>
                
                {/* Progress bar */}
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${getTraitColor(value, confidence)}`}
                    style={{ width: `${normalizedValue}%` }}
                  />
                </div>
                
                {/* Interpretation */}
                <p className="text-xs text-gray-600">
                  {getTraitInterpretation(trait as keyof typeof TRAIT_INFO, value, confidence)}
                </p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Current Policy Plan */}
      {personalityState.policy_plan.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Current Adaptation Strategy
          </h3>
          <div className="space-y-2">
            {personalityState.policy_plan.map((policy, index) => (
              <div
                key={index}
                className="flex items-start space-x-2 p-2 bg-blue-50 rounded-md border border-blue-100"
              >
                <div className="flex-shrink-0 w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
                  {index + 1}
                </div>
                <span className="text-sm text-blue-800 leading-relaxed">
                  {policy}
                </span>
              </div>
            ))}
          </div>
          
          <div className="mt-3 text-xs text-gray-600">
            💡 The AI is using these behavioral guidelines to adapt its communication style to your personality.
          </div>
        </div>
      )}

      {/* Trait Descriptions */}
      <div className="bg-white rounded-lg shadow-sm border p-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          About OCEAN Traits
        </h3>
        <div className="space-y-3 text-xs text-gray-600">
          {Object.entries(TRAIT_INFO).map(([trait, info]) => (
            <div key={trait}>
              <div className="font-medium text-gray-800 mb-1">
                {info.name}
              </div>
              <div>{info.description}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Detection Status */}
      <div className="bg-white rounded-lg shadow-sm border p-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">
          Detection Status
        </h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Overall Confidence:</span>
            <span className="font-medium">
              {Math.round(Object.values(personalityState.confidence_scores).reduce((a, b) => a + b, 0) / 5 * 100)}%
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Traits Above Threshold:</span>
            <span className="font-medium">
              {Object.values(personalityState.ocean).filter(v => Math.abs(v) > 0.3).length}/5
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Stability Status:</span>
            <span className={`font-medium ${
              personalityState.stable ? 'text-green-600' : 'text-yellow-600'
            }`}>
              {personalityState.stable ? 'Stable' : 'Still Learning'}
            </span>
          </div>
        </div>
        
        {!personalityState.stable && (
          <div className="mt-3 text-xs text-gray-600">
            💭 Keep chatting! The AI needs more conversation to accurately detect your personality traits.
          </div>
        )}
      </div>
    </div>
  );
}
















