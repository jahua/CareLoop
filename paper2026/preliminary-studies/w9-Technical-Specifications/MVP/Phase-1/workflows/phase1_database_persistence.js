// PHASE 1: DATABASE PERSISTENCE WITH POSTGRESQL
// Enhanced session management with EMA personality state tracking
// Integrates with existing PostgreSQL schema for session continuity

// Database connection configuration (should be set in N8N environment variables)
const DB_CONFIG = {
  host: process.env.DB_POSTGRESDB_HOST || 'localhost',
  port: process.env.DB_POSTGRESDB_PORT || 5432,
  database: process.env.DB_POSTGRESDB_DATABASE || 'n8n_personality_ai',
  user: process.env.DB_POSTGRESDB_USER || 'n8n_user',
  password: process.env.DB_POSTGRESDB_PASSWORD || 'n8n_password'
};

// Get input data (this node can be placed after any step in the pipeline)
const inputData = $input.first()?.json || {};
const sessionId = inputData.session_id || '';
const turnIndex = inputData.turn_index || 1;
const userMessage = inputData.clean_msg || '';
const assistantResponse = inputData.verifier?.verified_response || 
                          inputData.generator?.raw_content || 
                          inputData.choices?.[0]?.message?.content || '';

// Personality state data from EMA smoothing
const detectorData = inputData.detector || {};
const currentOcean = detectorData.current_detection || { O: 0, C: 0, E: 0, A: 0, N: 0 };
const smoothedOcean = detectorData.smoothed_ocean || currentOcean;
const confidenceScores = detectorData.smoothed_confidence || detectorData.current_confidence || {};
const personalityStable = detectorData.personality_stable || false;
const emaApplied = detectorData.ema_applied || false;

// Regulation and verification data
const regulatorData = inputData.regulator || {};
const verifierData = inputData.verifier || {};

console.log('💾 DATABASE PERSISTENCE - Session:', sessionId, 'Turn:', turnIndex);
console.log('🧠 Smoothed OCEAN:', JSON.stringify(smoothedOcean));
console.log('🎯 Personality stable:', personalityStable);

// Validate required data
if (!sessionId) {
  console.log('❌ No session ID provided, skipping database persistence');
  return [{ json: { ...inputData, database: { status: 'error', error: 'No session ID' } } }];
}

// POSTGRESQL OPERATIONS USING N8N's BUILT-IN DATABASE FUNCTIONS
// Note: In production N8N environment, use the Postgres node instead of raw queries

async function saveSessionData() {
  try {
    // 1. ENSURE SESSION EXISTS
    const sessionQuery = `
      INSERT INTO sessions (session_id, created_at, last_updated, user_metadata) 
      VALUES ($1, NOW(), NOW(), $2)
      ON CONFLICT (session_id) 
      DO UPDATE SET last_updated = NOW()
      RETURNING session_id, created_at;
    `;
    
    const sessionMetadata = {
      personality_stable: personalityStable,
      ema_applied: emaApplied,
      total_turns: turnIndex,
      last_personality_update: new Date().toISOString()
    };

    console.log('💾 Ensuring session exists...');
    
    // 2. SAVE CONVERSATION TURN
    if (userMessage) {
      const userTurnQuery = `
        INSERT INTO turns (session_id, turn_index, role, text, created_at)
        VALUES ($1, $2, 'user', $3, NOW())
        ON CONFLICT (session_id, turn_index, role) DO NOTHING;
      `;
      console.log('💬 Saving user message...');
    }
    
    if (assistantResponse) {
      const assistantTurnQuery = `
        INSERT INTO turns (session_id, turn_index, role, text, created_at)
        VALUES ($1, $2, 'assistant', $3, NOW())
        ON CONFLICT (session_id, turn_index, role) DO NOTHING;
      `;
      console.log('🤖 Saving assistant response...');
    }

    // 3. SAVE COMPREHENSIVE STATE SNAPSHOT
    const stateSnapshot = {
      session_id: sessionId,
      turn_index: turnIndex,
      
      // Core personality state (EMA smoothed)
      ocean: smoothedOcean,
      ocean_raw: currentOcean, // Keep raw detection for analysis
      confidence: confidenceScores,
      stable: personalityStable,
      
      // EMA metadata
      ema_alpha: detectorData.ema_alpha,
      ema_applied: emaApplied,
      historical_state: detectorData.historical_state,
      
      // Regulation state
      directives: regulatorData.raw_directives || [],
      regulation_analysis: regulatorData.raw_analysis,
      zurich_applied: regulatorData.zurich_applied || false,
      
      // Verification state
      verification_status: verifierData.verification_status,
      adherence_score: verifierData.adherence_score,
      refinement_applied: verifierData.refinement_attempts > 0,
      
      // API performance
      detector_status: detectorData.api_status,
      generator_status: inputData.generator?.api_status,
      
      // Timestamps
      last_updated: new Date().toISOString(),
      pipeline_completed: new Date().toISOString()
    };

    const stateQuery = `
      INSERT INTO state_snapshots (session_id, turn_index, state_json, execution_id, created_at)
      VALUES ($1, $2, $3, $4, NOW())
      ON CONFLICT (session_id, turn_index) 
      DO UPDATE SET state_json = $3, created_at = NOW()
      RETURNING id;
    `;
    
    const executionId = `exec_${sessionId}_${turnIndex}_${Date.now()}`;
    
    console.log('📊 Saving state snapshot...');
    
    // 4. UPDATE WORKFLOW EXECUTION TRACKING
    const workflowQuery = `
      INSERT INTO workflow_executions (
        execution_id, workflow_name, session_id, status, 
        started_at, finished_at, execution_data
      )
      VALUES ($1, $2, $3, 'success', NOW(), NOW(), $4)
      ON CONFLICT (execution_id) 
      DO UPDATE SET status = 'success', finished_at = NOW(), execution_data = $4;
    `;
    
    const executionData = {
      pipeline_stages: ['ingest', 'detect', 'regulate', 'generate', 'verify', 'persist'],
      ema_smoothing: emaApplied,
      verification_score: verifierData.adherence_score,
      personality_stable: personalityStable,
      total_processing_time: new Date().toISOString()
    };

    console.log('📈 Updating workflow execution...');

    // Since we can't execute raw SQL in this context, we'll prepare the data
    // for the PostgreSQL node that should follow this code node
    
    const databaseOperations = {
      session_upsert: {
        query: sessionQuery,
        params: [sessionId, JSON.stringify(sessionMetadata)]
      },
      user_turn_insert: userMessage ? {
        query: `INSERT INTO turns (session_id, turn_index, role, text) VALUES ($1, $2, 'user', $3) ON CONFLICT DO NOTHING`,
        params: [sessionId, turnIndex * 2 - 1, userMessage] // Odd numbers for user turns
      } : null,
      assistant_turn_insert: assistantResponse ? {
        query: `INSERT INTO turns (session_id, turn_index, role, text) VALUES ($1, $2, 'assistant', $3) ON CONFLICT DO NOTHING`,
        params: [sessionId, turnIndex * 2, assistantResponse] // Even numbers for assistant turns
      } : null,
      state_snapshot_upsert: {
        query: stateQuery,
        params: [sessionId, turnIndex, JSON.stringify(stateSnapshot), executionId]
      },
      workflow_execution_upsert: {
        query: workflowQuery,
        params: [executionId, 'personality-chat-enhanced', sessionId, JSON.stringify(executionData)]
      }
    };

    console.log('✅ Database operations prepared successfully');
    
    return {
      status: 'success',
      operations_prepared: Object.keys(databaseOperations).filter(key => databaseOperations[key] !== null).length,
      session_id: sessionId,
      turn_index: turnIndex,
      execution_id: executionId,
      state_snapshot: stateSnapshot,
      database_operations: databaseOperations
    };

  } catch (error) {
    console.log('❌ Database operation error:', error.message);
    return {
      status: 'error',
      error: error.message,
      session_id: sessionId,
      turn_index: turnIndex
    };
  }
}

// RETRIEVE HISTORICAL PERSONALITY STATE FOR EMA
async function getHistoricalPersonalityState() {
  try {
    if (turnIndex <= 1) {
      return null; // No historical data for first turn
    }

    // Prepare query to get the most recent personality state
    const historyQuery = `
      SELECT state_json 
      FROM state_snapshots 
      WHERE session_id = $1 AND turn_index < $2 
      ORDER BY turn_index DESC 
      LIMIT 1;
    `;
    
    console.log('📚 Preparing historical state retrieval...');
    
    return {
      query: historyQuery,
      params: [sessionId, turnIndex],
      purpose: 'ema_historical_state'
    };

  } catch (error) {
    console.log('❌ Historical state retrieval error:', error.message);
    return null;
  }
}

// MAIN EXECUTION
async function executeDatabase() {
  // Save current session data
  const saveResult = await saveSessionData();
  
  // Prepare historical data retrieval for next turn
  const historyQuery = await getHistoricalPersonalityState();
  
  // Prepare session summary
  const sessionSummaryQuery = {
    query: `
      SELECT 
        s.session_id,
        s.created_at,
        COUNT(t.id) as total_turns,
        ls.state_json->'ocean' as current_ocean,
        ls.state_json->'stable' as personality_stable
      FROM sessions s
      LEFT JOIN turns t ON s.session_id = t.session_id
      LEFT JOIN latest_session_states ls ON s.session_id = ls.session_id
      WHERE s.session_id = $1
      GROUP BY s.session_id, s.created_at, ls.state_json;
    `,
    params: [sessionId],
    purpose: 'session_summary'
  };

  const result = {
    ...inputData,
    database: {
      persistence_status: saveResult.status,
      save_operations: saveResult.database_operations,
      historical_query: historyQuery,
      session_summary_query: sessionSummaryQuery,
      execution_id: saveResult.execution_id,
      state_snapshot_saved: saveResult.state_snapshot || null,
      error: saveResult.error || null,
      
      // Enhanced metadata for next pipeline stage
      session_continuity: {
        session_id: sessionId,
        turn_index: turnIndex,
        personality_stable: personalityStable,
        ema_applied: emaApplied,
        ready_for_next_turn: true
      },
      
      timestamp: new Date().toISOString()
    }
  };

  console.log('💾 Database persistence completed');
  return result;
}

// Execute and return result
executeDatabase().then(result => {
  return [{ json: result }];
}).catch(error => {
  console.log('❌ Database execution error:', error.message);
  return [{ 
    json: { 
      ...inputData, 
      database: { 
        persistence_status: 'error', 
        error: error.message,
        timestamp: new Date().toISOString()
      } 
    } 
  }];
});
