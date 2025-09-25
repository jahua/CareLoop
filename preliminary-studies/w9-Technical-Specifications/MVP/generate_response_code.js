// Generate Response - Code Node Implementation
// Replace the "Generate Response" HTTP Request node with this Code node

// 1. Get required data from previous nodes
const JUGUANG_API_KEY = "sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u";
const policyPlan = $input.item.json.policy_plan;
const conversationContext = $input.item.json.conversation_context;

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
        content: `Generate a helpful response following these behavioral directives: ${JSON.stringify(policyPlan)}. CRITICAL REQUIREMENTS: 1) Only reference information explicitly mentioned in the conversation - do not introduce external facts or knowledge. 2) All statements must be grounded in the dialog context. 3) Cap questions at 1-2 maximum. 4) Keep response length appropriate (50-150 words typically). 5) Follow the personality-adapted directives while maintaining therapeutic helpfulness.`
      },
      {
        role: 'user',
        content: `Recent conversation:\n${conversationContext}\n\nGenerate an appropriate response that follows the behavioral directives and stays grounded in the conversation context.`
      }
    ],
    temperature: 0.7,
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
    throw new Error(`Generate Response API failed with status ${error.response.status}: ${JSON.stringify(error.response.data)}`);
  }
  throw new Error(`Generate Response request failed: ${error.message}`);
}
















