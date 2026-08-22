-- Minimal schema for the project skeleton.
-- Real tables (users, gift notes, etc.) land with their own features.

CREATE TABLE IF NOT EXISTS site_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- author_name is a temporary free-text stand-in for a real account —
-- gets replaced once Placeholder identity exists.
CREATE TABLE IF NOT EXISTS posts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL,
    body        TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
