// PHASE 1: VERIFICATION/REFINEMENT PIPELINE
// This node ensures directive adherence and validates response quality
// Implements automated refinement when responses don't meet personality-based criteria

const GPT4_API_KEY = 'sk-Njwkf6uCcvrJ3QTqga0UxizZTL7OMoshPlcniO3lTRuQqJBR';

// Verification Configuration
const MAX_REFINEMENT_ATTEMPTS = 2; // Maximum number of refinement iterations
const MIN_ADHERENCE_SCORE = 0.7; // Minimum score for directive adherence (0.0-1.0)
const REFINEMENT_TEMPERATURE = 0.5; // Temperature for refinement generation

// Get input data from the generator node
const inputData = $input.first()?.json || {};
const generatedResponse = inputData.generator?.raw_content || inputData.choices?.[0]?.message?.content || '';
const appliedDirectives = inputData.regulator?.raw_directives || inputData.directives || [];
const sessionId = inputData.session_id || '';
const userMessage = inputData.clean_msg || inputData.turn_text || '';
const oceanState = inputData.detector?.smoothed_ocean || inputData.ocean_disc || { O:0, C:0, E:0, A:0, N:0 };
const personalityStable = inputData.detector?.personality_stable || false;

console.log('🔍 VERIFICATION PIPELINE - Session:', sessionId);
console.log('📝 Response length:', generatedResponse.length);
console.log('🎯 Directives count:', appliedDirectives.length);
console.log('🧠 OCEAN state:', JSON.stringify(oceanState));

// Handle missing data
if (!generatedResponse || appliedDirectives.length === 0) {
  console.log('⚠️ Insufficient data for verification');
  const result = {
    ...inputData,
    verifier: {
      verification_status: 'insufficient_data',
      adherence_score: 0.0,
      refinement_needed: false,
      refinement_attempts: 0,
      verified_response: generatedResponse || 'Response unavailable',
      error: 'Missing response or directives for verification'
    }
  };
  return [{ json: result }];
}

// VERIFICATION PROMPT - Analyzes response against directives
const verificationPrompt = `You are a verification system for personality-adaptive responses. Evaluate how well the assistant's response follows the given personality-based behavioral directives.

**USER MESSAGE:**
"${userMessage}"

**DETECTED PERSONALITY TRAITS (OCEAN):**
${Object.entries(oceanState).map(([trait, value]) => `${trait}: ${value === 1 ? 'High' : value === -1 ? 'Low' : 'Neutral'}`).join(', ')}

**APPLIED BEHAVIORAL DIRECTIVES:**
${appliedDirectives.map((dir, i) => `${i + 1}. ${dir}`).join('\n')}

**ASSISTANT'S RESPONSE:**
"${generatedResponse}"

**VERIFICATION CRITERIA:**
1. **Directive Adherence**: Does the response follow each behavioral directive?
2. **Personality Consistency**: Is the response style consistent with detected traits?
3. **Therapeutic Appropriateness**: Is the response supportive and contextually appropriate?
4. **Grounding**: Does the response stay grounded in the user's message without hallucination?
5. **Length Constraint**: Is the response 70-150 words with ≤2 questions?

**SCORING**: Rate each criterion 0.0-1.0, then provide overall adherence score (0.0-1.0).

**OUTPUT FORMAT (JSON only):**
{
  "adherence_score": 0.0-1.0,
  "criterion_scores": {
    "directive_adherence": 0.0-1.0,
    "personality_consistency": 0.0-1.0,
    "therapeutic_appropriateness": 0.0-1.0,
    "grounding": 0.0-1.0,
    "length_constraint": 0.0-1.0
  },
  "issues_identified": ["issue1", "issue2"],
  "refinement_needed": true/false,
  "refinement_suggestions": ["suggestion1", "suggestion2"]
}`;

console.log('🔍 Running verification analysis...');

// Call GPT-4 for verification
const verificationOptions = {
  method: 'POST',
  url: 'https://api.nuwaapi.com/v1/chat/completions',
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${GPT4_API_KEY}`
  },
  body: JSON.stringify({
    model: 'gpt-4',
    messages: [{ role: 'user', content: verificationPrompt }],
    max_tokens: 500,
    temperature: 0.1
  }),
  timeout: 20000
};

let verificationResult = {};
let refinementNeeded = false;

try {
  const verificationResponse = await this.helpers.httpRequest(verificationOptions);
  
  if (verificationResponse.choices && verificationResponse.choices.length > 0) {
    let verificationContent = verificationResponse.choices[0].message.content;
    console.log('✅ Verification analysis completed');
    
    // Parse verification JSON
    let cleanedVerification = verificationContent.trim();
    cleanedVerification = cleanedVerification.replace(/```[a-zA-Z]*\s*|\s*```/gi, '').trim();
    const verificationMatch = cleanedVerification.match(/\{[\s\S]*\}/);
    if (verificationMatch) {
      cleanedVerification = verificationMatch[0];
    }
    
    try {
      verificationResult = JSON.parse(cleanedVerification);
      console.log('📊 Adherence score:', verificationResult.adherence_score);
      
      refinementNeeded = verificationResult.refinement_needed || 
                        (verificationResult.adherence_score < MIN_ADHERENCE_SCORE);
      
    } catch (parseError) {
      console.log('⚠️ Verification JSON parsing failed, assuming refinement needed');
      verificationResult = {
        adherence_score: 0.5,
        refinement_needed: true,
        issues_identified: ['Verification parsing failed'],
        refinement_suggestions: ['Review response for directive adherence']
      };
      refinementNeeded = true;
    }
    
  } else {
    console.log('❌ No verification response from API');
    refinementNeeded = true; // Default to refinement if verification fails
  }
  
} catch (error) {
  console.log('❌ Verification API error:', error.message);
  refinementNeeded = true; // Default to refinement on error
}

// REFINEMENT LOGIC
let finalResponse = generatedResponse;
let refinementAttempts = 0;
let refinementHistory = [];

if (refinementNeeded && refinementAttempts < MAX_REFINEMENT_ATTEMPTS) {
  console.log('🔧 Response requires refinement, attempting improvement...');
  
  const refinementPrompt = `You are a response refinement system. Improve the assistant's response to better follow the personality-based behavioral directives while maintaining therapeutic appropriateness.

**USER MESSAGE:**
"${userMessage}"

**PERSONALITY TRAITS:**
${Object.entries(oceanState).map(([trait, value]) => `${trait}: ${value === 1 ? 'High' : value === -1 ? 'Low' : 'Neutral'}`).join(', ')}

**BEHAVIORAL DIRECTIVES TO FOLLOW:**
${appliedDirectives.map((dir, i) => `${i + 1}. ${dir}`).join('\n')}

**CURRENT RESPONSE (needs improvement):**
"${generatedResponse}"

**IDENTIFIED ISSUES:**
${verificationResult.issues_identified ? verificationResult.issues_identified.join(', ') : 'General adherence improvement needed'}

**REFINEMENT GUIDELINES:**
- Follow all behavioral directives precisely
- Maintain 70-150 word length
- Include ≤2 questions maximum
- Stay grounded in user's message
- Keep therapeutic and supportive tone
- Match personality-appropriate communication style

**REFINED RESPONSE (text only, no JSON):**`;

  try {
    const refinementOptions = {
      method: 'POST',
      url: 'https://api.nuwaapi.com/v1/chat/completions',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GPT4_API_KEY}`
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [{ role: 'user', content: refinementPrompt }],
        max_tokens: 250,
        temperature: REFINEMENT_TEMPERATURE
      }),
      timeout: 20000
    };
    
    const refinementResponse = await this.helpers.httpRequest(refinementOptions);
    
    if (refinementResponse.choices && refinementResponse.choices.length > 0) {
      const refinedContent = refinementResponse.choices[0].message.content.trim();
      console.log('✅ Response refinement completed');
      console.log('📝 Refined response length:', refinedContent.length);
      
      finalResponse = refinedContent;
      refinementAttempts++;
      
      refinementHistory.push({
        attempt: refinementAttempts,
        original: generatedResponse,
        refined: refinedContent,
        issues_addressed: verificationResult.issues_identified || [],
        timestamp: new Date().toISOString()
      });
      
    } else {
      console.log('⚠️ Refinement failed, using original response');
    }
    
  } catch (refinementError) {
    console.log('❌ Refinement error:', refinementError.message);
  }
}

// Final verification status
const finalVerificationStatus = refinementNeeded ? 
  (refinementAttempts > 0 ? 'refined' : 'needs_refinement') : 
  'verified';

console.log('🎯 Final verification status:', finalVerificationStatus);
console.log('🔧 Refinement attempts:', refinementAttempts);

// Update the result with verification and refinement data
const result = {
  ...inputData,
  verifier: {
    verification_status: finalVerificationStatus,
    adherence_score: verificationResult.adherence_score || 0.5,
    criterion_scores: verificationResult.criterion_scores || {},
    refinement_needed: refinementNeeded,
    refinement_attempts: refinementAttempts,
    max_attempts: MAX_REFINEMENT_ATTEMPTS,
    min_adherence_score: MIN_ADHERENCE_SCORE,
    issues_identified: verificationResult.issues_identified || [],
    refinement_suggestions: verificationResult.refinement_suggestions || [],
    refinement_history: refinementHistory,
    original_response: generatedResponse,
    verified_response: finalResponse,
    directives_evaluated: appliedDirectives,
    personality_stable: personalityStable,
    timestamp: new Date().toISOString()
  },
  // Update the generator output with the verified/refined response
  generator: {
    ...inputData.generator,
    verified_content: finalResponse,
    verification_applied: true
  },
  // Legacy compatibility
  choices: [{ message: { content: finalResponse } }],
  final_response: finalResponse
};

console.log('✅ Verification/Refinement pipeline completed');

return [{ json: result }];
