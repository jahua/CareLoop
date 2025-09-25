// N8N Code Node JavaScript - Juguang API Call
// NOTE: This approach requires the Code node to have access to this.helpers
// which may not be available in all N8N versions/configurations

// Get conversation context from input
const conversationContext = $input.item.json.conversation_context;
const JUGUANG_API_KEY = "sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u";

// Define request options
const options = {
  method: 'POST',
  url: 'https://ai.juguang.chat/v1/chat/completions',
  headers: {
    'Authorization': `Bearer ${JUGUANG_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: {
    model: 'gemini-1.5-flash',
    messages: [
      {
        role: 'system',
        content: 'Analyze this conversation to infer OCEAN personality traits. Return JSON only with this exact format: {"ocean": {"O": float, "C": float, "E": float, "A": float, "N": float}, "trait_conf": {"O": float, "C": float, "E": float, "A": float, "N": float}, "evidence_quotes": [string, ...]}. Values in [-1,1], confidence in [0,1]. Base analysis on conversation patterns, word choice, and communication style. No prose commentary.'
      },
      {
        role: 'user',
        content: `Conversation:\n${conversationContext}`
      }
    ],
    response_format: {
      type: 'json_object'
    },
    temperature: 0.3
  }
};

try {
  // Use N8N's built-in HTTP helper (if available)
  const response = await this.helpers.httpRequest(options);
  
  // Return the response data
  return response;
  
} catch (error) {
  // Enhanced error handling
  if (error.response) {
    throw new Error(`API request failed with status ${error.response.status}: ${JSON.stringify(error.response.data)}`);
  }
  throw new Error(`Request failed: ${error.message}`);
}
















