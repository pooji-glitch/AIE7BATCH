-- Initialize the credit_assistant database
CREATE DATABASE IF NOT EXISTS credit_assistant;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_credit_analyses_user_id ON credit_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_credit_analyses_created_at ON credit_analyses(created_at);
CREATE INDEX IF NOT EXISTS idx_chat_messages_user_id ON chat_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_what_if_scenarios_user_id ON what_if_scenarios(user_id);

-- Create views for analytics
CREATE OR REPLACE VIEW user_analytics AS
SELECT 
    u.id as user_id,
    u.name,
    u.email,
    COUNT(ca.id) as total_analyses,
    AVG(ca.credit_score) as avg_credit_score,
    MAX(ca.credit_score) as max_credit_score,
    MIN(ca.credit_score) as min_credit_score,
    COUNT(cm.id) as total_questions,
    COUNT(wis.id) as total_scenarios
FROM users u
LEFT JOIN credit_analyses ca ON u.id = ca.user_id
LEFT JOIN chat_messages cm ON u.id = cm.user_id
LEFT JOIN what_if_scenarios wis ON u.id = wis.user_id
GROUP BY u.id, u.name, u.email;

-- Create materialized view for dashboard stats
CREATE MATERIALIZED VIEW dashboard_stats AS
SELECT 
    COUNT(DISTINCT u.id) as total_users,
    COUNT(ca.id) as total_analyses,
    AVG(ca.credit_score) as avg_credit_score,
    COUNT(cm.id) as total_questions,
    COUNT(wis.id) as total_scenarios,
    DATE_TRUNC('day', ca.created_at) as date
FROM users u
LEFT JOIN credit_analyses ca ON u.id = ca.user_id
LEFT JOIN chat_messages cm ON u.id = cm.user_id
LEFT JOIN what_if_scenarios wis ON u.id = wis.user_id
GROUP BY DATE_TRUNC('day', ca.created_at);

-- Create function to refresh materialized view
CREATE OR REPLACE FUNCTION refresh_dashboard_stats()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW dashboard_stats;
END;
$$ LANGUAGE plpgsql;

-- Create function to get user credit trend
CREATE OR REPLACE FUNCTION get_user_credit_trend(user_id_param INTEGER)
RETURNS TABLE (
    date DATE,
    credit_score INTEGER,
    trend VARCHAR(10)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ca.created_at::DATE as date,
        ca.credit_score,
        CASE 
            WHEN LAG(ca.credit_score) OVER (ORDER BY ca.created_at) < ca.credit_score THEN 'UP'
            WHEN LAG(ca.credit_score) OVER (ORDER BY ca.created_at) > ca.credit_score THEN 'DOWN'
            ELSE 'STABLE'
        END as trend
    FROM credit_analyses ca
    WHERE ca.user_id = user_id_param
    ORDER BY ca.created_at;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE credit_assistant TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
