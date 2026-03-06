-- =============================================
-- PostgreSQL Schema for Personality-Adaptive AI Chatbot
-- Phase 1: Enhanced Workflow with Real EMA Smoothing
-- =============================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS performance_metrics CASCADE;
DROP TABLE IF EXISTS personality_states CASCADE;
DROP TABLE IF EXISTS conversation_turns CASCADE;
DROP TABLE IF EXISTS chat_sessions CASCADE;

-- =============================================
-- 1. Chat Sessions Table
-- =============================================
CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY,
    total_turns INTEGER DEFAULT 0,
    evaluation_mode BOOLEAN DEFAULT FALSE,
    baseline_comparison BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_created ON chat_sessions(created_at);
CREATE INDEX idx_sessions_status ON chat_sessions(status);

-- =============================================
-- 2. Conversation Turns Table
-- =============================================
CREATE TABLE conversation_turns (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    turn_index INTEGER NOT NULL,
    user_message TEXT,
    assistant_response TEXT,
    directives_applied JSONB DEFAULT '[]',
    verification_status VARCHAR(20),
    adherence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, turn_index)
);

CREATE INDEX idx_turns_session ON conversation_turns(session_id);
CREATE INDEX idx_turns_created ON conversation_turns(created_at);

-- =============================================
-- 3. Personality States Table
-- =============================================
CREATE TABLE personality_states (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    turn_index INTEGER NOT NULL,
    ocean_o FLOAT,
    ocean_c FLOAT,
    ocean_e FLOAT,
    ocean_a FLOAT,
    ocean_n FLOAT,
    confidence_o FLOAT,
    confidence_c FLOAT,
    confidence_e FLOAT,
    confidence_a FLOAT,
    confidence_n FLOAT,
    stable BOOLEAN DEFAULT FALSE,
    ema_applied BOOLEAN DEFAULT FALSE,
    emotional_state VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, turn_index)
);

CREATE INDEX idx_personality_session ON personality_states(session_id);
CREATE INDEX idx_personality_stable ON personality_states(stable);
CREATE INDEX idx_personality_created ON personality_states(created_at);

-- =============================================
-- 4. Performance Metrics Table
-- =============================================
CREATE TABLE performance_metrics (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    turn_index INTEGER NOT NULL,
    detector_status VARCHAR(20),
    regulator_status VARCHAR(20),
    generator_status VARCHAR(20),
    verifier_status VARCHAR(20),
    database_status VARCHAR(20),
    total_processing_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, turn_index)
);

CREATE INDEX idx_metrics_session ON performance_metrics(session_id);
CREATE INDEX idx_metrics_created ON performance_metrics(created_at);

-- =============================================
-- 5. Helper Function: Get Latest Personality State
-- =============================================
CREATE OR REPLACE FUNCTION get_latest_personality_state(p_session_id UUID)
RETURNS TABLE(
    ocean_o FLOAT,
    ocean_c FLOAT,
    ocean_e FLOAT,
    ocean_a FLOAT,
    ocean_n FLOAT,
    confidence_o FLOAT,
    confidence_c FLOAT,
    confidence_e FLOAT,
    confidence_a FLOAT,
    confidence_n FLOAT,
    stable BOOLEAN,
    turn_index INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ps.ocean_o,
        ps.ocean_c,
        ps.ocean_e,
        ps.ocean_a,
        ps.ocean_n,
        ps.confidence_o,
        ps.confidence_c,
        ps.confidence_e,
        ps.confidence_a,
        ps.confidence_n,
        ps.stable,
        ps.turn_index
    FROM personality_states ps
    WHERE ps.session_id = p_session_id
    ORDER BY ps.turn_index DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- 6. Helper Function: Get Conversation History
-- =============================================
CREATE OR REPLACE FUNCTION get_conversation_history(p_session_id UUID, p_limit INTEGER DEFAULT 10)
RETURNS TABLE(
    turn_index INTEGER,
    user_message TEXT,
    assistant_response TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ct.turn_index,
        ct.user_message,
        ct.assistant_response,
        ct.created_at
    FROM conversation_turns ct
    WHERE ct.session_id = p_session_id
    ORDER BY ct.turn_index DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- 7. View: Session Summary
-- =============================================
CREATE OR REPLACE VIEW session_summary AS
SELECT 
    cs.session_id,
    cs.total_turns,
    cs.evaluation_mode,
    cs.status,
    ps.stable as personality_stable,
    ps.ocean_o, ps.ocean_c, ps.ocean_e, ps.ocean_a, ps.ocean_n,
    cs.created_at,
    cs.updated_at
FROM chat_sessions cs
LEFT JOIN LATERAL (
    SELECT * FROM personality_states 
    WHERE session_id = cs.session_id 
    ORDER BY turn_index DESC 
    LIMIT 1
) ps ON true;

-- =============================================
-- 8. Trigger: Update session timestamp
-- =============================================
CREATE OR REPLACE FUNCTION update_session_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE chat_sessions 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE session_id = NEW.session_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_session_on_turn
AFTER INSERT ON conversation_turns
FOR EACH ROW
EXECUTE FUNCTION update_session_timestamp();

-- =============================================
-- Schema Setup Complete
-- =============================================
-- Verify tables
SELECT 'Schema created successfully!' as status;
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND (
    tablename = 'chat_sessions' OR
    tablename = 'conversation_turns' OR
    tablename = 'personality_states' OR
    tablename = 'performance_metrics'
) ORDER BY tablename;









































