-- Database initialization script for N8N Personality AI System
-- Based on technical specifications from w9-Technical-Specifications.md

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Core session management
CREATE TABLE IF NOT EXISTS sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW(),
    user_metadata JSONB DEFAULT '{}'::jsonb
);

-- Individual conversation turns
CREATE TABLE IF NOT EXISTS turns (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES sessions(session_id) ON DELETE CASCADE,
    turn_index INTEGER NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
    text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Authoritative state snapshots (main state storage)
CREATE TABLE IF NOT EXISTS state_snapshots (
    id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES sessions(session_id) ON DELETE CASCADE,
    turn_index INTEGER NOT NULL,
    state_json JSONB NOT NULL,
    execution_id VARCHAR(255), -- N8N execution ID for traceability
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Ensure one state per turn per session
    UNIQUE(session_id, turn_index)
);

-- N8N workflow executions tracking (optional, for enhanced monitoring)
CREATE TABLE IF NOT EXISTS workflow_executions (
    id SERIAL PRIMARY KEY,
    execution_id VARCHAR(255) UNIQUE NOT NULL,
    workflow_name VARCHAR(255) NOT NULL,
    session_id UUID REFERENCES sessions(session_id),
    status VARCHAR(50) NOT NULL, -- 'running', 'success', 'error', 'waiting'
    started_at TIMESTAMP DEFAULT NOW(),
    finished_at TIMESTAMP,
    error_message TEXT,
    execution_data JSONB,
    
    -- Performance metrics
    total_duration_ms INTEGER,
    node_timings JSONB
);

-- Performance indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_snapshots_session_turn ON state_snapshots(session_id, turn_index);
CREATE INDEX IF NOT EXISTS idx_turns_session_created ON turns(session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_sessions_updated ON sessions(last_updated);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_session ON workflow_executions(session_id);
CREATE INDEX IF NOT EXISTS idx_workflow_executions_status ON workflow_executions(status);

-- Indexes for JSONB queries (personality state lookups)
CREATE INDEX IF NOT EXISTS idx_state_snapshots_ocean ON state_snapshots USING GIN ((state_json->'ocean'));
CREATE INDEX IF NOT EXISTS idx_state_snapshots_stable ON state_snapshots USING GIN ((state_json->'stable'));

-- Function to update session timestamp
CREATE OR REPLACE FUNCTION update_session_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE sessions 
    SET last_updated = NOW() 
    WHERE session_id = NEW.session_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-update session timestamp
DROP TRIGGER IF EXISTS trigger_update_session_timestamp ON state_snapshots;
CREATE TRIGGER trigger_update_session_timestamp
    AFTER INSERT OR UPDATE ON state_snapshots
    FOR EACH ROW
    EXECUTE FUNCTION update_session_timestamp();

-- Insert sample data for testing
INSERT INTO sessions (session_id) VALUES (uuid_generate_v4()) ON CONFLICT DO NOTHING;

-- View for latest session states (convenient for queries)
CREATE OR REPLACE VIEW latest_session_states AS
SELECT DISTINCT ON (session_id) 
    session_id,
    turn_index,
    state_json,
    execution_id,
    created_at
FROM state_snapshots
ORDER BY session_id, turn_index DESC;

-- View for session summaries
CREATE OR REPLACE VIEW session_summaries AS
SELECT 
    s.session_id,
    s.created_at,
    s.last_updated,
    COUNT(t.id) as total_turns,
    ls.state_json->'ocean' as current_ocean,
    ls.state_json->'stable' as personality_stable,
    ls.turn_index as last_turn_index
FROM sessions s
LEFT JOIN turns t ON s.session_id = t.session_id
LEFT JOIN latest_session_states ls ON s.session_id = ls.session_id
GROUP BY s.session_id, s.created_at, s.last_updated, ls.state_json, ls.turn_index;

-- Function to get session history (used by N8N workflow)
CREATE OR REPLACE FUNCTION get_session_history(p_session_id UUID, p_limit INTEGER DEFAULT 20)
RETURNS TABLE (
    role VARCHAR(10),
    text TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.role,
        t.text,
        t.created_at
    FROM turns t
    WHERE t.session_id = p_session_id
    ORDER BY t.created_at DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- Function to get latest personality state
CREATE OR REPLACE FUNCTION get_latest_personality_state(p_session_id UUID)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    SELECT state_json INTO result
    FROM state_snapshots
    WHERE session_id = p_session_id
    ORDER BY turn_index DESC
    LIMIT 1;
    
    RETURN COALESCE(result, '{"ocean": {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}, "stable": false}'::jsonb);
END;
$$ LANGUAGE plpgsql;

-- Grant permissions for N8N database user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO n8n_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO n8n_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO n8n_user;

-- Insert some sample data for development/testing
DO $$
DECLARE
    sample_session_id UUID;
BEGIN
    -- Create a sample session
    INSERT INTO sessions (session_id) 
    VALUES (uuid_generate_v4()) 
    RETURNING session_id INTO sample_session_id;
    
    -- Add some sample conversation turns
    INSERT INTO turns (session_id, turn_index, role, text) VALUES
    (sample_session_id, 1, 'user', 'Hello, I''m feeling a bit anxious about my upcoming presentation.'),
    (sample_session_id, 2, 'assistant', 'I understand that presentations can feel overwhelming. What specific aspects are making you feel most anxious?'),
    (sample_session_id, 3, 'user', 'I worry about forgetting what to say and stumbling over my words.'),
    (sample_session_id, 4, 'assistant', 'Those are very common concerns. Have you had a chance to practice your presentation out loud?');
    
    -- Add sample state snapshot
    INSERT INTO state_snapshots (session_id, turn_index, state_json) VALUES
    (sample_session_id, 4, jsonb_build_object(
        'session_id', sample_session_id,
        'turn_index', 4,
        'ocean', jsonb_build_object('O', 0.2, 'C', -0.1, 'E', -0.3, 'A', 0.4, 'N', 0.5),
        'trait_conf', jsonb_build_object('O', 0.65, 'C', 0.58, 'E', 0.72, 'A', 0.68, 'N', 0.75),
        'stable', false,
        'policy_plan', jsonb_build_array('validate concerns warmly', 'use gentle hedging', 'ask one supportive question'),
        'flags', jsonb_build_object('refined_once', false, 'neutral_fallback', false),
        'last_updated', NOW()
    ));
END $$;

COMMIT;
















