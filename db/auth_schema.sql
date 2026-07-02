
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    hashed_pass TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS auth_sessions (
    session_id TEXT PRIMARY KEY,    -- Store SHA256 Hash of token, already high entropy from secret's token gen
    user_id TEXT,
    created_at DATE NOT NULL,
    expiry DATE NOT NULL,       -- For absolute timeouts
    ip_address TEXT,            -- Optional
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- TODO: Add session refer to OWASP cheatsheet