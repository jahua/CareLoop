// PHASE 1: WEBHOOK API ENDPOINTS
// Real-time API endpoints for personality-adaptive chatbot system
// Provides REST API interface for external applications and frontend integration

const express = require('express');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const axios = require('axios');

// API Configuration
const API_PORT = process.env.API_PORT || 3001;
const N8N_WEBHOOK_BASE_URL = process.env.N8N_WEBHOOK_URL || 'http://localhost:5678';
const N8N_API_KEY = process.env.N8N_API_KEY || '';

// Database configuration (for direct queries when needed)
const DB_CONFIG = {
  host: process.env.DB_POSTGRESDB_HOST || 'localhost',
  port: process.env.DB_POSTGRESDB_PORT || 5432,
  database: process.env.DB_POSTGRESDB_DATABASE || 'n8n_personality_ai',
  user: process.env.DB_POSTGRESDB_USER || 'n8n_user',
  password: process.env.DB_POSTGRESDB_PASSWORD || 'n8n_password'
};

// Initialize Express app
const app = express();

// Middleware
app.use(cors({
  origin: function(origin, callback) {
    // Allow requests from any localhost port during development
    const allowedOrigins = [
      'http://localhost:3000',
      'http://localhost:3001', 
      'http://localhost:3002',
      'http://localhost:3003',
      process.env.FRONTEND_URL
    ].filter(Boolean);
    
    if (!origin || allowedOrigins.some(allowed => origin.startsWith('http://localhost'))) {
      callback(null, true);
    } else if (allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// ===============================
// CORE CHAT API ENDPOINTS
// ===============================

/**
 * POST /api/chat/message
 * Process a single message through the enhanced personality pipeline
 */
app.post('/api/chat/message', async (req, res) => {
  try {
    const { session_id, message, user_metadata = {} } = req.body;
    
    if (!message || message.trim().length === 0) {
      return res.status(400).json({
        error: 'Message is required',
        code: 'MISSING_MESSAGE'
      });
    }

    // Generate session ID if not provided
    const sessionId = session_id || uuidv4();
    
    // Get turn index from database or start at 1
    const turnIndex = await getCurrentTurnIndex(sessionId) + 1;
    
    console.log(`💬 Processing message for session ${sessionId}, turn ${turnIndex}`);

    // Prepare payload for N8N enhanced workflow
    const workflowPayload = {
      session_id: sessionId,
      turn_index: turnIndex,
      evaluation_mode: false,
      baseline_comparison: false,
      messages: [
        {
          turn: 1,
          role: 'assistant',
          content: "I'm here to listen and support you. How are you feeling today?"
        },
        {
          turn: 2,
          role: 'user',
          content: message
        }
      ],
      user_metadata: user_metadata,
      api_request: true,
      timestamp: new Date().toISOString()
    };

    // Call N8N enhanced workflow
    const workflowResponse = await callN8NWorkflow('personality-chat-enhanced', workflowPayload);
    
    if (workflowResponse.success) {
      const result = workflowResponse.data;
      
      // Format response for API
      const response = {
        session_id: sessionId,
        turn_index: turnIndex,
        message: {
          role: 'assistant',
          content: result.verifier?.verified_response || result.reply || 'I apologize, but I encountered an issue processing your message.',
          timestamp: new Date().toISOString()
        },
        personality_state: {
          ocean: result.detector?.smoothed_ocean || result.ocean_disc || { O: 0, C: 0, E: 0, A: 0, N: 0 },
          confidence: result.detector?.smoothed_confidence || {},
          stable: result.detector?.personality_stable || false,
          ema_applied: result.detector?.ema_applied || false
        },
        regulation: {
          directives: result.regulator?.raw_directives || result.directives || [],
          analysis: result.regulator?.raw_analysis || {}
        },
        verification: {
          status: result.verifier?.verification_status || 'unknown',
          adherence_score: result.verifier?.adherence_score || 0.0,
          refinement_applied: (result.verifier?.refinement_attempts || 0) > 0
        },
        pipeline_status: {
          detector: result.detector?.api_status || 'unknown',
          regulator: result.regulator?.regulation_status || 'unknown',
          generator: result.generator?.api_status || 'unknown',
          verifier: result.verifier?.verification_status || 'unknown',
          database: result.database?.persistence_status || 'unknown'
        }
      };

      res.json(response);
    } else {
      throw new Error(workflowResponse.error || 'Workflow execution failed');
    }

  } catch (error) {
    console.error('❌ Chat message processing error:', error.message);
    res.status(500).json({
      error: 'Failed to process message',
      details: error.message,
      code: 'PROCESSING_ERROR'
    });
  }
});

/**
 * GET /api/chat/session/:sessionId
 * Retrieve session information and conversation history
 */
app.get('/api/chat/session/:sessionId', async (req, res) => {
  try {
    const { sessionId } = req.params;
    const { limit = 20 } = req.query;

    console.log(`📚 Retrieving session ${sessionId}`);

    // Get session data from database
    const sessionData = await getSessionData(sessionId, parseInt(limit));
    
    if (!sessionData) {
      return res.status(404).json({
        error: 'Session not found',
        code: 'SESSION_NOT_FOUND'
      });
    }

    res.json(sessionData);

  } catch (error) {
    console.error('❌ Session retrieval error:', error.message);
    res.status(500).json({
      error: 'Failed to retrieve session',
      details: error.message,
      code: 'RETRIEVAL_ERROR'
    });
  }
});

/**
 * POST /api/chat/session
 * Create a new chat session
 */
app.post('/api/chat/session', async (req, res) => {
  try {
    const { user_metadata = {} } = req.body;
    const sessionId = uuidv4();

    console.log(`🆕 Creating new session ${sessionId}`);

    // Initialize session in database
    await createSession(sessionId, user_metadata);

    res.json({
      session_id: sessionId,
      created_at: new Date().toISOString(),
      user_metadata: user_metadata,
      status: 'created'
    });

  } catch (error) {
    console.error('❌ Session creation error:', error.message);
    res.status(500).json({
      error: 'Failed to create session',
      details: error.message,
      code: 'CREATION_ERROR'
    });
  }
});

// ===============================
// PERSONALITY STATE API ENDPOINTS
// ===============================

/**
 * GET /api/personality/state/:sessionId
 * Get current personality state for a session
 */
app.get('/api/personality/state/:sessionId', async (req, res) => {
  try {
    const { sessionId } = req.params;

    console.log(`🧠 Retrieving personality state for ${sessionId}`);

    const personalityState = await getPersonalityState(sessionId);
    
    if (!personalityState) {
      return res.status(404).json({
        error: 'Personality state not found',
        code: 'STATE_NOT_FOUND'
      });
    }

    res.json(personalityState);

  } catch (error) {
    console.error('❌ Personality state retrieval error:', error.message);
    res.status(500).json({
      error: 'Failed to retrieve personality state',
      details: error.message,
      code: 'STATE_RETRIEVAL_ERROR'
    });
  }
});

/**
 * GET /api/personality/history/:sessionId
 * Get personality evolution history for a session
 */
app.get('/api/personality/history/:sessionId', async (req, res) => {
  try {
    const { sessionId } = req.params;
    const { limit = 10 } = req.query;

    console.log(`📊 Retrieving personality history for ${sessionId}`);

    const personalityHistory = await getPersonalityHistory(sessionId, parseInt(limit));
    
    res.json({
      session_id: sessionId,
      history: personalityHistory,
      total_snapshots: personalityHistory.length
    });

  } catch (error) {
    console.error('❌ Personality history retrieval error:', error.message);
    res.status(500).json({
      error: 'Failed to retrieve personality history',
      details: error.message,
      code: 'HISTORY_RETRIEVAL_ERROR'
    });
  }
});

// ===============================
// SYSTEM STATUS AND HEALTH ENDPOINTS
// ===============================

/**
 * GET /api/health
 * System health check
 */
app.get('/api/health', async (req, res) => {
  try {
    const health = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0-phase1',
      services: {
        api: 'healthy',
        database: 'checking',
        n8n: 'checking'
      }
    };

    // Check database connection
    try {
      await testDatabaseConnection();
      health.services.database = 'healthy';
    } catch (dbError) {
      health.services.database = 'unhealthy';
      health.status = 'degraded';
    }

    // Check N8N connection
    try {
      await testN8NConnection();
      health.services.n8n = 'healthy';
    } catch (n8nError) {
      health.services.n8n = 'unhealthy';
      health.status = 'degraded';
    }

    const statusCode = health.status === 'healthy' ? 200 : 503;
    res.status(statusCode).json(health);

  } catch (error) {
    res.status(500).json({
      status: 'unhealthy',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * GET /api/stats
 * System statistics and metrics
 */
app.get('/api/stats', async (req, res) => {
  try {
    const stats = await getSystemStats();
    res.json(stats);
  } catch (error) {
    console.error('❌ Stats retrieval error:', error.message);
    res.status(500).json({
      error: 'Failed to retrieve stats',
      details: error.message
    });
  }
});

// ===============================
// HELPER FUNCTIONS
// ===============================

async function callN8NWorkflow(workflowName, payload) {
  try {
    const response = await axios.post(`${N8N_WEBHOOK_BASE_URL}/webhook/${workflowName}`, payload, {
      headers: {
        'Content-Type': 'application/json',
        ...(N8N_API_KEY && { 'Authorization': `Bearer ${N8N_API_KEY}` })
      },
      timeout: 30000
    });

    return {
      success: true,
      data: response.data
    };
  } catch (error) {
    console.error('❌ N8N workflow call error:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

async function getCurrentTurnIndex(sessionId) {
  // This would query the database for the current turn index
  // For now, return a placeholder
  return 0;
}

async function getSessionData(sessionId, limit) {
  // Query database for session data
  // Return formatted session information
  return {
    session_id: sessionId,
    created_at: new Date().toISOString(),
    conversation: [],
    personality_state: {},
    total_turns: 0
  };
}

async function createSession(sessionId, userMetadata) {
  // Create new session in database
  console.log(`Creating session ${sessionId} with metadata:`, userMetadata);
}

async function getPersonalityState(sessionId) {
  // Query latest personality state from database
  return {
    session_id: sessionId,
    ocean: { O: 0, C: 0, E: 0, A: 0, N: 0 },
    confidence: {},
    stable: false,
    last_updated: new Date().toISOString()
  };
}

async function getPersonalityHistory(sessionId, limit) {
  // Query personality evolution history
  return [];
}

async function testDatabaseConnection() {
  // Test database connectivity
  return true;
}

async function testN8NConnection() {
  // Test N8N connectivity
  return true;
}

async function getSystemStats() {
  return {
    uptime: process.uptime(),
    memory_usage: process.memoryUsage(),
    active_sessions: 0,
    total_messages_processed: 0,
    avg_response_time: 0,
    timestamp: new Date().toISOString()
  };
}

// ===============================
// ERROR HANDLING AND SERVER START
// ===============================

// Global error handler
app.use((error, req, res, next) => {
  console.error('❌ Unhandled error:', error);
  res.status(500).json({
    error: 'Internal server error',
    code: 'INTERNAL_ERROR'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
    code: 'NOT_FOUND'
  });
});

// Start server
const server = app.listen(API_PORT, () => {
  console.log(`🚀 Phase 1 Webhook API Server running on port ${API_PORT}`);
  console.log(`📡 N8N Webhook Base URL: ${N8N_WEBHOOK_BASE_URL}`);
  console.log(`💾 Database: ${DB_CONFIG.host}:${DB_CONFIG.port}/${DB_CONFIG.database}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('✅ API server closed');
    process.exit(0);
  });
});

module.exports = app;
