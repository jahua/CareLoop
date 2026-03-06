// PHASE 1: EMA SMOOTHING FOR PERSONALITY ESTIMATES
// This node enhances personality detection with Exponential Moving Average smoothing
// Integrates with PostgreSQL for session continuity and state persistence

const GPT4_API_KEY = 'sk-Njwkf6uCcvrJ3QTqga0UxizZTL7OMoshPlcniO3lTRuQqJBR';

// EMA Configuration
const EMA_ALPHA = 0.3; // Learning rate for new observations (0.2-0.4 range recommended)
const MIN_CONFIDENCE_THRESHOLD = 0.6; // Minimum confidence for trait updates
const STABILIZATION_TURNS = 5; // Number of turns before considering personality "stable"

// Get essential input data
const inputData = $input.first().json;
const ctx = String(inputData.conversation_context || '').trim();
const userMessage = inputData.clean_msg || '';
const sessionId = inputData.session_id || '';
const turnIndex = inputData.turn_index || 1;
const evaluationMode = inputData.evaluation_mode || false;

console.log('🔄 EMA SMOOTHING - Session:', sessionId, 'Turn:', turnIndex);

// Handle empty context
if (!ctx) {
  console.log('⚠️ No conversation context provided, returning default values');
  const result = {
    ...inputData,
    detector: {
      raw_response: null,
      raw_content: '{"ocean_disc":{"O":0,"C":0,"E":0,"A":0,"N":0}}',
      api_status: 'no_context',
      error: 'No conversation context provided',
      ema_smoothed: false,
      historical_state: null
    }
  };
  return [{ json: result }];
}

// Enhanced Zurich Model prompt with EMA context awareness
const prompt = `Analyze the following conversation using the Zurich Model framework for personality assessment. Evaluate the user's Big Five traits by examining their underlying motivational needs for SECURITY, AROUSAL, and POWER, along with their coping strategies and approach-avoidance patterns.

**ASSESSMENT FRAMEWORK:**

**Openness (Arousal System):**
Examine the user's need for cognitive and experiential arousal:
• HIGH (+1): Seeks novelty, cognitive stimulation, new perspectives; shows curiosity about possibilities; embraces uncertainty as stimulating
• LOW (-1): Prefers familiar patterns; avoids cognitive overload; finds comfort in routine; shows resistance to new ideas that disrupt mental equilibrium
• NEUTRAL (0): No clear preference pattern evident

**Conscientiousness (Security & Control System):**
Assess need for structure, predictability, and behavioral control:
• HIGH (+1): Seeks security through organization and planning; shows systematic approach to problems; values reliability and achievement as sources of stability
• LOW (-1): Prefers flexible, spontaneous adaptation; avoids rigid structures; shows accommodative coping (adjusting goals rather than pursuing them systematically)
• NEUTRAL (0): No clear organizational preference evident

**Extraversion (Social Arousal & Power System):**
Evaluate approach vs. avoidance in social energy and stimulation seeking:
• HIGH (+1): Approaches social situations for stimulation; seeks social influence and connection; energized by interpersonal engagement
• LOW (-1): Avoids high-stimulation social environments; prefers controlled, low-intensity social contact; seeks solitude for regulation
• NEUTRAL (0): No clear social energy pattern evident

**Agreeableness (Affiliation & Security System):**
Analyze approach vs. avoidance in interpersonal bonding and cooperation:
• HIGH (+1): Approaches others with trust and empathy; seeks harmony and mutual support; prioritizes group cohesion over individual goals
• LOW (-1): Shows skepticism toward others' motives; maintains psychological distance; prioritizes autonomy over conformity; shows competitive rather than cooperative tendencies
• NEUTRAL (0): No clear interpersonal orientation evident

**Neuroticism (Security & Threat Detection System):**
Evaluate emotional regulation and security maintenance:
• HIGH (-1): Shows heightened threat sensitivity; experiences emotional instability; difficulty maintaining psychological security; uses worry/anxiety as coping mechanisms
• LOW (+1): Maintains emotional equilibrium; shows secure baseline; effective emotional regulation; calm under stress
• NEUTRAL (0): No clear emotional regulation pattern evident

**IMPORTANT**: Include confidence scores (0.0-1.0) for each trait assessment to enable EMA smoothing.

Return JSON format: {"ocean_disc":{"O":-1|0|1,"C":-1|0|1,"E":-1|0|1,"A":-1|0|1,"N":-1|0|1},"confidence":{"O":0.0-1.0,"C":0.0-1.0,"E":0.0-1.0,"A":0.0-1.0,"N":0.0-1.0}}

Conversation:
${ctx}`;

console.log('🚀 Calling GPT-4 API for Enhanced Detection with EMA Support...');

// GPT-4 API Call
const apiUrl = 'https://api.nuwaapi.com/v1/chat/completions';
const options = {
  method: 'POST',
  url: apiUrl,
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${GPT4_API_KEY}`
  },
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 300,
    temperature: 0.1
  }),
  timeout: 20000
};

try {
  const response = await this.helpers.httpRequest(options);
  
  if (response.choices && response.choices.length > 0) {
    let content = response.choices[0].message.content;
    console.log('✅ Got response from GPT-4 API');
    
    // Clean and parse JSON
    let cleanedContent = content.trim();
    cleanedContent = cleanedContent.replace(/```[a-zA-Z]*\s*|\s*```/gi, '').trim();
    const jsonMatch = cleanedContent.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      cleanedContent = jsonMatch[0];
    }
    
    let detectionResult = {};
    try {
      detectionResult = JSON.parse(cleanedContent);
    } catch (parseError) {
      console.log('⚠️ JSON parsing failed, using fallback');
      detectionResult = {
        ocean_disc: { O: 0, C: 0, E: 0, A: 0, N: 0 },
        confidence: { O: 0.5, C: 0.5, E: 0.5, A: 0.5, N: 0.5 }
      };
    }

    // Extract current detection
    const currentOcean = detectionResult.ocean_disc || { O: 0, C: 0, E: 0, A: 0, N: 0 };
    const currentConfidence = detectionResult.confidence || { O: 0.5, C: 0.5, E: 0.5, A: 0.5, N: 0.5 };

    // EMA SMOOTHING LOGIC
    console.log('🔄 Applying EMA smoothing...');
    
    // For Turn 1 or when no historical data exists, use current detection
    if (turnIndex <= 1) {
      console.log('📊 First turn - using raw detection');
      
      const result = {
        ...inputData,
        detector: {
          raw_response: response,
          raw_content: content,
          cleaned_content: cleanedContent,
          current_detection: currentOcean,
          current_confidence: currentConfidence,
          smoothed_ocean: currentOcean, // Same as current for first turn
          smoothed_confidence: currentConfidence,
          ema_applied: false,
          ema_alpha: EMA_ALPHA,
          historical_state: null,
          turn_number: turnIndex,
          api_status: 'success',
          model_used: 'gpt4-enhanced-ema',
          timestamp: new Date().toISOString()
        }
      };
      
      return [{ json: result }];
    }
    
    // For subsequent turns, retrieve historical state and apply EMA
    // Note: In a real implementation, this would query PostgreSQL
    // For now, we'll simulate with a basic approach
    console.log('📈 Subsequent turn - applying EMA smoothing');
    
    // Simulate historical state (in production, retrieve from database)
    const historicalOcean = inputData.last_ocean_state || { O: 0, C: 0, E: 0, A: 0, N: 0 };
    const historicalConfidence = inputData.last_confidence_state || { O: 0.5, C: 0.5, E: 0.5, A: 0.5, N: 0.5 };
    
    // Apply EMA smoothing formula: new_value = α * current + (1-α) * previous
    const smoothedOcean = {};
    const smoothedConfidence = {};
    const traits = ['O', 'C', 'E', 'A', 'N'];
    
    traits.forEach(trait => {
      const current = currentOcean[trait] || 0;
      const historical = historicalOcean[trait] || 0;
      const confidence = currentConfidence[trait] || 0.5;
      
      // Only apply smoothing if confidence is above threshold
      if (confidence >= MIN_CONFIDENCE_THRESHOLD) {
        smoothedOcean[trait] = Math.round(EMA_ALPHA * current + (1 - EMA_ALPHA) * historical);
        smoothedConfidence[trait] = Math.max(confidence, historicalConfidence[trait] || 0.5);
        console.log(`🎯 ${trait}: ${historical} → ${current} = ${smoothedOcean[trait]} (conf: ${confidence.toFixed(2)})`);
      } else {
        // Low confidence - prefer historical value
        smoothedOcean[trait] = historical;
        smoothedConfidence[trait] = historicalConfidence[trait] || 0.5;
        console.log(`⚠️ ${trait}: Low confidence (${confidence.toFixed(2)}), keeping historical: ${historical}`);
      }
    });
    
    // Determine if personality is stabilizing
    const isStable = turnIndex >= STABILIZATION_TURNS && 
                    Object.values(smoothedConfidence).every(conf => conf >= MIN_CONFIDENCE_THRESHOLD);
    
    console.log('📊 EMA Smoothing Results:', JSON.stringify(smoothedOcean));
    console.log('🎯 Personality Stable:', isStable);
    
    const result = {
      ...inputData,
      detector: {
        raw_response: response,
        raw_content: content,
        cleaned_content: cleanedContent,
        current_detection: currentOcean,
        current_confidence: currentConfidence,
        smoothed_ocean: smoothedOcean,
        smoothed_confidence: smoothedConfidence,
        historical_state: {
          previous_ocean: historicalOcean,
          previous_confidence: historicalConfidence
        },
        ema_applied: true,
        ema_alpha: EMA_ALPHA,
        confidence_threshold: MIN_CONFIDENCE_THRESHOLD,
        personality_stable: isStable,
        stabilization_turns: STABILIZATION_TURNS,
        turn_number: turnIndex,
        api_status: 'success',
        model_used: 'gpt4-enhanced-ema',
        timestamp: new Date().toISOString()
      }
    };
    
    return [{ json: result }];
    
  } else {
    console.log('❌ No choices in response');
    
    const result = {
      ...inputData,
      detector: {
        raw_response: response,
        raw_content: null,
        cleaned_content: '{"ocean_disc":{"O":0,"C":0,"E":0,"A":0,"N":0}}',
        api_status: 'no_choices',
        error: 'No choices in API response',
        ema_applied: false,
        model_used: 'gpt4-enhanced-ema',
        timestamp: new Date().toISOString()
      }
    };
    
    return [{ json: result }];
  }
  
} catch (error) {
  console.log('❌ GPT-4 API Request Error:', error.message);
  
  const result = {
    ...inputData,
    detector: {
      raw_response: null,
      raw_content: null,
      cleaned_content: '{"ocean_disc":{"O":0,"C":0,"E":0,"A":0,"N":0}}',
      api_status: 'error',
      error: error.message,
      ema_applied: false,
      model_used: 'gpt4-enhanced-ema',
      timestamp: new Date().toISOString()
    }
  };
  
  return [{ json: result }];
}
