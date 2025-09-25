// Refine Response - Code Node Implementation
// Replace the "Refine Response" HTTP Request node with this Code node

// 1. Get required data from previous nodes
const JUGUANG_API_KEY = "sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u";
const draftReply = $input.item.json.draft_reply;
const reasons = $input.item.json.reasons;

// 2. Define the request options for N8N's httpRequest helper
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
        content: `Fix this response based on these issues: ${JSON.stringify(reasons)}. ONLY make minimal adjustments to address the specific problems. Do not add new content or claims. Keep the response grounded in the original conversation context. Maintain the helpful and appropriate tone.`
      },
      {
        role: 'user',
        content: `Original response to fix:\n${draftReply}`
      }
    ],
    temperature: 0.3,
    max_tokens: 200
  }
};

// 3. Use N8N's built-in HTTP helper method
try {
  const response = await this.helpers.httpRequest(options);
  
  // 4. Return the response data for the next node
  return response;

} catch (error) {
  // Enhanced error handling
  if (error.response) {
    throw new Error(`Refine Response API failed with status ${error.response.status}: ${JSON.stringify(error.response.data)}`);
  }
  throw new Error(`Refine Response request failed: ${error.message}`);
}
















