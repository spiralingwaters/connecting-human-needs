INSERT OR IGNORE INTO site_meta (key, value)
VALUES ('tagline', 'The world already has enough. What it lacks is circulation.');

INSERT INTO posts (author_name, body)
SELECT 'welcome', 'Welcome to the stream — say what you need and what you have.'
WHERE NOT EXISTS (SELECT 1 FROM posts);
