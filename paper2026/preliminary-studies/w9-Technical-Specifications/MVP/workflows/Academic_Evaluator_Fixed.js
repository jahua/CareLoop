// ACADEMIC EVALUATOR SYSTEM - Fixed for N8N Code Node
// Based on Samuel's 3-EVALUATOR-GPT-SYSTEM-PROMPT.md
// Implements comprehensive evaluation criteria for chatbot conversation assessment

const GEMINI_API_KEY = 'AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E';

// Get conversation data from previous nodes
const responseData = $json || {};
const regulationData = ($items('Build Regulation Directives (Comprehensive Zurich Algorithm)', 'main', 0)?.json) || {};
const detectionData = ($items('Parse Detection JSON (Enhanced Debug)', 'main', 0)?.json) || {};
const inputData = ($items('Ingest (Evaluation Enhanced)', 'main', 0)?.json) || {};

console.log('🎓 Academic Evaluator - Processing conversation turn...');
console.log('📊 Input data available:', !!inputData);
console.log('🧠 Detection data available:', !!detectionData);
console.log('🎯 Regulation data available:', !!regulationData);
console.log('💬 Response data available:', !!responseData);

// Extract conversation components with fallbacks
const sessionId = inputData.session_id || 'eval-001';
const assistantStart = inputData.assistant_start || "I'm here to listen and support you. How are you feeling today?";
const userMessage = inputData.clean_msg || inputData.message || '';
const assistantReply = responseData.reply || responseData.final_response || responseData.response || '';
const oceanDetected = detectionData.ocean_disc || regulationData.ocean_disc || { O:0,C:0,E:0,A:0,N:0 };
const regulationDirectives = regulationData.directives || [];

console.log('📝 Session:', sessionId);
console.log('👤 User message:', userMessage.substring(0, 50) + '...');
console.log('🤖 Assistant reply:', assistantReply.substring(0, 50) + '...');
console.log('🧠 OCEAN detected:', JSON.stringify(oceanDetected));
console.log('🎯 Directives applied:', regulationDirectives.length);

// EVALUATOR SYSTEM PROMPT (Based on Samuel's Research)
const evaluatorPrompt = `You are an unbiased, methodical evaluator for chatbot conversations within an academic master's thesis context.

You assess responses based on Big Five personality-aware chatbot behavior regulation effectiveness.

**CONVERSATION TO EVALUATE:**
- Assistant Start: "${assistantStart}"
- User Message: "${userMessage}"
- Assistant Reply: "${assistantReply}"
- Detected Personality (O,C,E,A,N): ${JSON.stringify(oceanDetected)}
- Regulation Directives Applied: ${regulationDirectives.join('; ')}

**PERSONALITY TRAITS UNDERSTANDING:**
- Openness (O): High (+1) = Curious, imaginative; Low (-1) = Prefers routine, resistant to new ideas
- Conscientiousness (C): High (+1) = Organized, disciplined; Low (-1) = Disorganized, impulsive
- Extraversion (E): High (+1) = Outgoing, energetic; Low (-1) = Reserved, quiet, withdrawn
- Agreeableness (A): High (+1) = Cooperative, empathetic; Low (-1) = Critical, skeptical, confrontational
- Neuroticism (N): High (+1) = Emotionally stable, calm; Low (-1) = Anxious, emotionally sensitive

**EVALUATION CRITERIA (Answer Yes/No/Not Sure for each):**
1. Detection Accurate: Does the personality detection match the user's expressed traits?
2. Regulation Effective: Were the correct regulation prompts applied based on detected traits?
3. Emotional Tone Appropriate: Does the response match the user's emotional state and traits?
4. Relevance & Coherence: Is the response relevant, logical, and context-aware?
5. Personality Needs Addressed: Does the response address personality-specific emotional needs?

**OUTPUT FORMAT - Provide ONLY this JSON structure:**
{
  "msg_no": 1,
  "assistant_start": "[assistant start message]",
  "user_reply": "[user message]", 
  "assistant_reply": "[assistant response]",
  "detection_accurate": "Yes/No/Not Sure",
  "regulation_effective": "Yes/No/Not Sure",
  "emotional_tone_appropriate": "Yes/No/Not Sure",
  "relevance_coherence": "Yes/No/Not Sure",
  "personality_needs_addressed": "Yes/No/Not Sure",
  "evaluator_notes": "[Detailed analysis with specific justifications for each rating]"
}`;

// Function to create fallback evaluation
function createFallbackEvaluation(error = null) {
  return {
    session_id: sessionId,
    msg_no: 1,
    assistant_start_base: assistantStart,
    user_reply_base: userMessage,
    assistant_reply_base: assistantReply,
    emotional_tone_appropriate_base: 'Not Sure',
    relevance_coherence_base: 'Not Sure',
    personality_needs_addressed_base: 'Not Sure',
    evaluator_notes_base: error ? `Evaluation error: ${error}` : 'Evaluation service unavailable',
    detected_personality: oceanDetected,
    regulation_directives_applied: regulationDirectives,
    detection_accurate: 'Not Sure',
    regulation_effective: 'Not Sure',
    evaluation_timestamp: new Date().toISOString(),
    evaluation_api_used: 'fallback',
    evaluation_error: error || 'No evaluation performed'
  };
}

// Check if we have minimum required data
if (!userMessage && !assistantReply) {
  console.log('⚠️ Insufficient data for evaluation');
  return [{ json: createFallbackEvaluation('Insufficient conversation data') }];
}

console.log('🎓 Calling Gemini API for academic evaluation...');

// API Configuration
const model = 'gemini-1.5-flash';
const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${GEMINI_API_KEY}`;

const options = {
  method: 'POST',
  url: apiUrl,
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    contents: [{ parts: [{ text: evaluatorPrompt }] }],
    generationConfig: {
      temperature: 0.1,
      maxOutputTokens: 1000,
      topK: 40,
      topP: 0.95
    },
    safetySettings: [
      { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_MEDIUM_AND_ABOVE' },
      { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_MEDIUM_AND_ABOVE' },
      { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_MEDIUM_AND_ABOVE' },
      { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_MEDIUM_AND_ABOVE' }
    ]
  }),
  timeout: 30000
};

try {
  console.log('📡 Making evaluation API request...');
  const response = await this.helpers.httpRequest(options);
  
  if (response.candidates && response.candidates.length > 0) {
    let content = response.candidates[0].content.parts[0].text;
    console.log('✅ Evaluation API successful');
    console.log('📝 Raw evaluation content length:', content.length);
    
    // Clean JSON extraction
    let cleanedContent = content;
    if (content.includes('```')) {
      cleanedContent = content.replace(/```json\s*|\s*```/g, '').trim();
      console.log('🧹 Cleaned content from markdown blocks');
    }
    
    // Parse evaluation JSON
    try {
      const evaluationResult = JSON.parse(cleanedContent);
      console.log('✅ Evaluation JSON parsed successfully');
      
      // Structure final output
      const evaluationOutput = {
        session_id: sessionId,
        msg_no: 1,
        assistant_start_base: assistantStart,
        user_reply_base: userMessage,
        assistant_reply_base: assistantReply,
        emotional_tone_appropriate_base: evaluationResult.emotional_tone_appropriate || 'Not Sure',
        relevance_coherence_base: evaluationResult.relevance_coherence || 'Not Sure',
        personality_needs_addressed_base: evaluationResult.personality_needs_addressed || 'Not Sure',
        evaluator_notes_base: evaluationResult.evaluator_notes || 'Evaluation completed',
        
        // Additional metadata for research
        detected_personality: oceanDetected,
        regulation_directives_applied: regulationDirectives,
        detection_accurate: evaluationResult.detection_accurate || 'Not Sure',
        regulation_effective: evaluationResult.regulation_effective || 'Not Sure',
        evaluation_timestamp: new Date().toISOString(),
        evaluation_api_used: model,
        evaluation_status: 'success'
      };
      
      console.log('🎓 Final Evaluation Output structured successfully');
      
      // CRITICAL: Return array with json property for N8N
      return [{ json: evaluationOutput }];
      
    } catch (jsonError) {
      console.log('⚠️ JSON parsing failed:', jsonError.message);
      console.log('🔄 Using fallback evaluation');
      
      return [{ json: createFallbackEvaluation(`JSON parsing failed: ${jsonError.message}`) }];
    }
    
  } else {
    console.log('❌ No candidates in evaluation response');
    
    // Check for safety blocking
    if (response.promptFeedback && response.promptFeedback.blockReason) {
      const reason = response.promptFeedback.blockReason;
      console.log(`🛡️ Evaluation blocked by safety filters: ${reason}`);
      return [{ json: createFallbackEvaluation(`Safety filter: ${reason}`) }];
    }
    
    return [{ json: createFallbackEvaluation('No candidates returned from API') }];
  }
  
} catch (error) {
  console.log('❌ Evaluation API Error:', error.message);
  
  return [{ json: createFallbackEvaluation(error.message) }];
}





















