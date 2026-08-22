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
-- existed; new posts fill both it and author_id. kind='redemption' marks
-- the one public announcement a gift note ever makes (SiteShape.md step 4).
CREATE TABLE IF NOT EXISTS posts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL,
    author_id   INTEGER REFERENCES users(id),
    body        TEXT NOT NULL,
    kind        TEXT NOT NULL DEFAULT 'post',
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- A gift note: authored, held, passed, and redeemed (SiteShape.md steps 1-4).
-- redeemed_at is set once and the note is then final — no more passing.
CREATE TABLE IF NOT EXISTS gift_notes (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    title               TEXT NOT NULL,
    description         TEXT NOT NULL,
    contact_info        TEXT NOT NULL,
    original_author_id  INTEGER NOT NULL REFERENCES users(id),
    current_holder_id   INTEGER NOT NULL REFERENCES users(id),
    expires_at          TEXT NOT NULL,
    redeemed_at         TEXT,
    created_at          TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- Minimal stand-in for a real private message, same spirit as gift_notes'
-- recipient-by-username field — folds into Private messaging once that
-- feature exists.
CREATE TABLE IF NOT EXISTS notifications (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    message    TEXT NOT NULL,
    is_read    INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
