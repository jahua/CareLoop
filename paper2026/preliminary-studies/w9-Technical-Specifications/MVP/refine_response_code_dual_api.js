// Refine Response - Dual API Code Node Implementation  
// Uses Gemini Pro API directly with Juguang fallback
// Replace the "Refine Response" HTTP Request node with this Code node

// 1. API Configuration
const GEMINI_API_KEY = "AIzaSyCu7cMyJAB4ossEePGYQQGpzjlqAfbIG2E";
const JUGUANG_API_KEY = "sk-nU7RSKnbZIOwH607r3MfbW5HmP6NIaj1aGVPFGcNDDiL0h5u";

// 2. Get required data from previous nodes
const draftReply = $input.item.json.draft_reply;
const reasons = $input.item.json.reasons;

// 3. Function to call Gemini Pro API directly
async function callGeminiDirect(prompt) {
  const options = {
    method: 'POST',
    url: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${GEMINI_API_KEY}`,
    headers: {
      'Content-Type': 'application/json'
    },
    body: {
      contents: [
        {
          parts: [
            {
              text: prompt
            }
          ]
        }
      ],
      generationConfig: {
        temperature: 0.3,
        maxOutputTokens: 200,
        topK: 40,
        topP: 0.95
      },
      safetySettings: [
        {
          category: "HARM_CATEGORY_HARASSMENT",
          threshold: "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
          category: "HARM_CATEGORY_HATE_SPEECH",
          threshold: "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
          category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
          threshold: "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
          category: "HARM_CATEGORY_DANGEROUS_CONTENT",
          threshold: "BLOCK_MEDIUM_AND_ABOVE"
        }
      ]
    }
  };

  const response = await this.helpers.httpRequest(options);
  
  // Extract content from Gemini response format
  if (response.candidates && response.candidates.length > 0) {
    const content = response.candidates[0].content.parts[0].text;
    return {
      choices: [
        {
          message: {
            content: content
          }
        }
      ],
      api_used: "gemini_direct"
    };
  }
  
  throw new Error("No valid response from Gemini Direct API");
}

// 4. Function to call Juguang API as fallback
async function callJuguangFallback(prompt) {
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

  const response = await this.helpers.httpRequest(options);
  return {
    ...response,
    api_used: "juguang_fallback"
  };
}

// 5. Create the unified prompt for both APIs
const refinementPrompt = `Fix this response based on these issues: ${JSON.stringify(reasons)}. ONLY make minimal adjustments to address the specific problems. Do not add new content or claims. Keep the response grounded in the original conversation context. Maintain the helpful and appropriate tone.

Original response to fix:
${draftReply}`;

// 6. Main execution with dual API logic
try {
  console.log("🚀 Attempting Gemini Pro Direct API for refinement...");
  const response = await callGeminiDirect(refinementPrompt);
  console.log("✅ Gemini Pro Direct API refinement successful");
  return response;

} catch (geminiError) {
  console.log("⚠️ Gemini Direct API failed, trying Juguang fallback:", geminiError.message);
  
  try {
    const response = await callJuguangFallback(refinementPrompt);
    console.log("✅ Juguang fallback API refinement successful");
    return response;
    
  } catch (juguangError) {
    console.log("❌ Both APIs failed for refinement");
    throw new Error(`All APIs failed - Gemini: ${geminiError.message}, Juguang: ${juguangError.message}`);
  }
}
