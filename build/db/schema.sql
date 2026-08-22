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

-- A gift note: authored + held only for now (SiteShape.md steps 1-2).
-- Passing/redeeming/expiring further are Note passing's job.
CREATE TABLE IF NOT EXISTS gift_notes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    title               TEXT NOT NULL,
    description         TEXT NOT NULL,
    contact_info        TEXT NOT NULL,
    original_author_id  INTEGER NOT NULL REFERENCES users(id),
    current_holder_id   INTEGER NOT NULL REFERENCES users(id),
    expires_at          TEXT NOT NULL,
    created_at          TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
