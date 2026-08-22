-- Minimal schema for the project skeleton.
-- Real tables (users, gift notes, etc.) land with their own features.

CREATE TABLE IF NOT EXISTS site_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- Placeholder identity: a stand-in for the eventual PNG-drawing login.
-- Only a hash of the random key is stored, never the key itself, mirroring
-- the hash-of-the-PNG pattern the real login will use later. No recovery
-- by design — losing the key loses the account.
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL UNIQUE,
    key_hash   TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- author_name is kept for old rows created before Placeholder identity
-- existed; new posts fill both it and author_id.
CREATE TABLE IF NOT EXISTS posts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL,
    author_id   INTEGER REFERENCES users(id),
    body        TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
