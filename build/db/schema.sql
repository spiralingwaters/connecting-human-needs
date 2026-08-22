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
-- is_bot marks a persona row: bots never sign up through /signup, they're
-- seeded directly, so key_hash on a bot row is never a real usable key.
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL UNIQUE,
    key_hash   TEXT NOT NULL,
    is_bot     INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- A bot persona's specialty + short prompt — the database is the bot's
-- memory, not a context window (Mission.md). No live LLM call reads
-- `prompt` yet; it's stored for when a later feature needs it.
CREATE TABLE IF NOT EXISTS bot_personas (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    specialty  TEXT NOT NULL,
    prompt     TEXT NOT NULL,
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

-- System notices (e.g. a note you authored was redeemed) — never a
-- conversation, so kept separate from message_threads/messages below.
CREATE TABLE IF NOT EXISTS notifications (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL REFERENCES users(id),
    message    TEXT NOT NULL,
    is_read    INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- is_bot_thread exists now as plumbing for the future Bot framework
-- feature; nothing populates it yet since no bot personas exist.
CREATE TABLE IF NOT EXISTS message_threads (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_a_id    INTEGER NOT NULL REFERENCES users(id),
    user_b_id    INTEGER NOT NULL REFERENCES users(id),
    is_bot_thread INTEGER NOT NULL DEFAULT 0,
    created_at   TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id  INTEGER NOT NULL REFERENCES message_threads(id),
    sender_id  INTEGER NOT NULL REFERENCES users(id),
    body       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

-- A silent, per-viewer filter only — never a platform-wide score or
-- punishment (Mission.md). Every query respecting a block must scope to
-- "as viewed by the current logged-in user," never a global exclusion.
CREATE TABLE IF NOT EXISTS blocks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    blocker_id INTEGER NOT NULL REFERENCES users(id),
    blocked_id INTEGER NOT NULL REFERENCES users(id),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    UNIQUE (blocker_id, blocked_id)
);
