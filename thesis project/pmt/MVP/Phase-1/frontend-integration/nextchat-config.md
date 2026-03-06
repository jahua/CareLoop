# NextChat Integration with Phase 1 Personality-Adaptive System

## Configuration for Personality Detection Workflow

### Environment Variables for Phase 1 Integration

```env
# Phase 1 Personality API Configuration
BASE_URL=http://localhost:3001/api
CUSTOM_MODELS=+personality-adaptive-gpt4,+ema-smoothed-claude,+therapeutic-assistant
DEFAULT_MODEL=personality-adaptive-gpt4

# Phase 1 Specific Settings
OPENAI_API_KEY=sk-Njwkf6uCcvrJ3QTqga0UxizZTL7OMoshPlcniO3lTRuQqJBR
CODE=phase1-personality-demo

# Enable advanced features for clinical use
ENABLE_BALANCE_QUERY=1
HIDE_USER_API_KEY=1
DISABLE_FAST_LINK=1

# Custom input template for personality detection
DEFAULT_INPUT_TEMPLATE="Please share how you're feeling today. The AI will adapt its communication style based on your personality traits detected through our conversation."

# Personality-specific model configurations
VISION_MODELS=personality-adaptive-gpt4,therapeutic-assistant
```

### Custom Model Integration

```javascript
// NextChat model configuration for Phase 1
const personalityModels = {
  "personality-adaptive-gpt4": {
    name: "Personality-Adaptive GPT-4",
    provider: "phase1",
    baseUrl: "http://localhost:3001/api/chat",
    features: ["ema-smoothing", "verification-pipeline", "therapeutic-adaptation"],
    description: "GPT-4 enhanced with personality detection and EMA smoothing"
  },
  "therapeutic-assistant": {
    name: "Therapeutic Assistant",
    provider: "phase1", 
    baseUrl: "http://localhost:3001/api/chat",
    features: ["clinical-validation", "crisis-support", "session-continuity"],
    description: "Specialized for therapeutic conversations with personality adaptation"
  }
};
```

## Multi-Agent Architecture Integration

### Agent Configuration

```typescript
interface PersonalityAgent {
  id: string;
  name: string;
  role: "detector" | "regulator" | "generator" | "verifier" | "coordinator";
  model: string;
  personalityFocus: "OCEAN" | "therapeutic" | "crisis" | "general";
  emaConfig: {
    alpha: number;
    confidenceThreshold: number;
    stabilizationTurns: number;
  };
}

const phase1Agents: PersonalityAgent[] = [
  {
    id: "personality-detector",
    name: "Personality Detection Agent",
    role: "detector",
    model: "personality-adaptive-gpt4",
    personalityFocus: "OCEAN",
    emaConfig: { alpha: 0.3, confidenceThreshold: 0.6, stabilizationTurns: 5 }
  },
  {
    id: "therapeutic-coordinator", 
    name: "Therapeutic Coordination Agent",
    role: "coordinator",
    model: "therapeutic-assistant",
    personalityFocus: "therapeutic",
    emaConfig: { alpha: 0.3, confidenceThreshold: 0.7, stabilizationTurns: 3 }
  },
  {
    id: "response-verifier",
    name: "Response Quality Verifier",
    role: "verifier", 
    model: "personality-adaptive-gpt4",
    personalityFocus: "general",
    emaConfig: { alpha: 0.3, confidenceThreshold: 0.8, stabilizationTurns: 2 }
  }
];
```
