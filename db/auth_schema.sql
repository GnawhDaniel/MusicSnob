
CREATE TABLE IF NOT EXISTS user (
    user_id TEXT PRIMARY KEY,
    hashed_pass TEXT NOT NULL
)

-- TODO: Add session refer to OWASP cheatsheet