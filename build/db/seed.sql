INSERT OR IGNORE INTO site_meta (key, value)
VALUES ('tagline', 'The world already has enough. What it lacks is circulation.');

INSERT INTO posts (author_name, body)
SELECT 'welcome', 'Welcome to the stream — say what you need and what you have.'
WHERE NOT EXISTS (SELECT 1 FROM posts);

-- Seeded bot persona: a sentinel image_hash (not a real SHA-256 hex
-- digest) since bots never sign up through /signup and nothing ever
-- needs to log in as one.
INSERT INTO users (username, image_hash, is_bot)
SELECT 'circulator', 'no-login-bot-account', 1
WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = 'circulator');

INSERT INTO bot_personas (user_id, specialty, prompt)
SELECT id, 'general welcome and circulation', 'You are Circulator, a plainly-labeled bot. Explain the pass-on-9-of-10 culture warmly and briefly when asked, and never claim to be human.'
FROM users
WHERE username = 'circulator'
  AND NOT EXISTS (SELECT 1 FROM bot_personas WHERE user_id = users.id);
