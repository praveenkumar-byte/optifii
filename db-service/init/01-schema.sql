-- Initialize the votes database schema
-- This runs automatically when the container starts for the first time

CREATE TABLE IF NOT EXISTS votes (
    id   VARCHAR(255) NOT NULL UNIQUE,
    vote VARCHAR(255) NOT NULL
);

-- Index for fast aggregation queries
CREATE INDEX IF NOT EXISTS idx_votes_vote ON votes(vote);

-- Seed data (optional, comment out if you want a clean start)
-- INSERT INTO votes (id, vote) VALUES ('seed-001', 'a'), ('seed-002', 'b');
