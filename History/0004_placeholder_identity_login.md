# Feature Summary

- [ ] Placeholder identity: signup hands out a random key the user copies; pasting it back logs them in. A plain stand-in for the PNG login, never called security.

## Description

Build the temporary stand-in identity system that the PNG-drawing login will eventually replace (Mission.md "PNG authorization is deferred until much later"). `/signup` picks a unique username and generates a long random key, shows it to the user once with a copy button and a clear "this is not secure, write it down, losing it loses the account" warning, and creates a `users` row (username, key_hash, created_at) — the raw key is never stored, only its hash, mirroring the eventual PNG-hash pattern even though this isn't real security. `/login` is a single field: paste the key, server hashes it and looks up the matching user, then starts a plain session (Flask session cookie storing user id). Once logged in, the site should show the username somewhere in the header and offer a logout link. The existing `/new` post form's free-text "poster name" field gets replaced: posting now requires being logged in, and `author_name` is looked up from the session instead of typed in — `/new` redirects to `/login` if no session exists. The `posts` table gets a nullable `author_id` column referencing `users.id` (kept alongside `author_name` for now, per Task history's note that the schema will need a real author reference) — new posts fill both; existing seeded/legacy posts keep author_name only.

- DB: new `users` table — id, username (unique), key_hash, created_at. `posts` gets `author_id INTEGER REFERENCES users(id)` (nullable, for old rows).
- `/signup` — GET shows username field; POST validates uniqueness, generates key, creates user, shows the key exactly once (never persisted anywhere retrievable).
- `/login` — GET shows a single key field; POST hashes + looks up, starts session, redirects to `/`.
- `/logout` — clears session, redirects to `/`.
- Header shows "logged in as @username" + logout link when a session exists, or Sign up / Log in links when not.
- `/new` requires a session; drop the free-text poster-name field entirely, use the session's username.
- No password reset, no email, no recovery — losing the key loses the account, matching the eventual PNG design's "no recovery, by design."
- Out of scope: the actual PNG doodle canvas/export (separate later features) — this only builds the key-based stand-in flow.

## To Do

## Done

- Added `users` table + `posts.author_id` column to schema.sql.
- Built `/signup` route + template (username form, one-time key reveal with copy button).
- Built `/login` route + template (key field, session start).
- Built `/logout` route.
- Updated header (base.html) to show logged-in state / auth links.
- Updated `/new` to require session, dropped free-text author name, uses session username + author_id.
- Existing seed post keeps working with a null author_id.
- Styled the signup/login forms, warning box, and key-reveal box consistently with existing forms.
- Verified with a scripted test-client run: signup issues a key and creates a user, duplicate username rejected, login with the right key starts a session, login with a wrong key fails, logged-out `/new` redirects to `/login`, logged-in `/new` posts under the session's username, header reflects logged-in state, logout clears the session and redirects appear again.

## Details

- Picked as the next feature per FeaturesList.md order and the dashboard's earlier "Start next: placeholder identity" quick-option note — Public feed intentionally jumped ahead of it, so this closes that gap.
- This is explicitly temporary/insecure by design (Mission.md + FeaturesList.md wording) — do not add password hashing best-practices, rate limiting, etc. beyond a plain hash lookup; that's over-engineering a stand-in that gets torn out for the real PNG system.
- Gift notes, Profiles, Private messaging, and Blocking all depend on real user identity — this feature unblocks all of them.
