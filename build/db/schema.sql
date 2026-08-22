-- Minimal schema for the project skeleton.
-- One table just to prove the DB read/write path works end to end.
-- Real tables (users, posts, gift notes, etc.) land with their own features.

CREATE TABLE IF NOT EXISTS site_meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
