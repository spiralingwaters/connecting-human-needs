# Feature Summary

- [ ] Signup: claim a unique username, check the image hash is unique, then release the PNG.

## Description

Replace Placeholder identity's key-based signup with the real flow Mission.md describes: "claim a unique username, check the image hash is unique, then release the PNG." This is the first of the two remaining routes (Signup, then Login) that actually replace Placeholder identity's stand-in — Placeholder identity's own FeaturesList.md wording calls it "a plain stand-in for the PNG login," so swapping it out now (rather than running two parallel auth systems) is the correct completion, not scope creep. `/signup` embeds the same drawing canvas built in Doodle canvas (username field + canvas + a "Claim & download my ID" button, replacing the old plain username-only form) directly on the page — no separate visit to `/id/draw` required, since the real flow is draw-then-claim-then-download in one sitting. On submit, the canvas's PNG bytes go to the server for hashing and a uniqueness check *before* anything is finalized: if the username or the image hash is already taken, nothing is created and the person can redraw/retry; only once both are confirmed unique does the server create the account and "release" the PNG back to the browser for download. Per Mission.md's hard privacy rule ("the server stores a hash of the ID image, never the image"), the raw uploaded bytes exist only for the duration of this one request — never written to disk — which also means Avatar derivation (crop-to-small-avatar) has to happen inline in this same request, since there's no later opportunity to touch the original image; that derived avatar file is what actually gets persisted (as its own small file), not the original drawing.

- DB: rename `users.key_hash` → `users.image_hash` (this is a dev database with no real users to migrate, so a clean rename is correct rather than carrying a legacy-named column) — still a hex SHA-256 hash of raw PNG bytes, same shape as before, different meaning.
- `/signup` GET: username field + the same canvas/toolbar from `/id/draw` (color swatches, eraser, clear) inline on the page.
- `/signup` POST: receives username + the canvas's PNG data (as a base64 data URL in a hidden field, populated by JS on submit) — server decodes it, computes `sha256` of the raw bytes, checks both username and image-hash uniqueness, and only on success inserts the user row and sends the welcome bot message (existing `send_welcome_message`, unchanged).
- On success, the browser (which already has the canvas data client-side) triggers the actual PNG download itself — the server's role is only to confirm uniqueness and create the account ("release" means "you're now allowed to keep this file," not a server-side file transfer).
- On failure (duplicate username or, vanishingly rarely, duplicate hash), show the specific error and let the canvas/username stay so the person can adjust and retry — no partial account is ever created.
- Avatar derivation (cropping the face-square region out of the raw bytes into a small stored avatar file) happens in this same request, before the raw bytes are discarded — implemented here because the schema/privacy rule forces it, but wiring the derived avatar into any UI display is explicitly Avatar derivation's task next, not this one.
- Bot seed data (`circulator`) needs an `image_hash` value that can never collide with a real upload — a fixed non-hex-sha256-shaped sentinel string works and documents itself as unmatchable.

## To Do

- Rename `users.key_hash` to `users.image_hash` in schema.sql; update the bot seed row in seed.sql to use a sentinel value under the new column name.
- Rewrite `/signup` template to include the canvas/toolbar (reuse `/id/draw`'s JS) plus the username field and a hidden field for the exported PNG data URL, submitted on a "Claim & download my ID" click.
- Rewrite `/signup`'s POST handler: decode the submitted PNG data, hash it, check username + hash uniqueness, insert the user row, derive+store a small avatar (crop the face-square region, resize down, save to `build/static/avatars/<user_id>.png`), send the welcome message, then respond in a way that lets the client-side download proceed (e.g. render a success state the page's JS uses to trigger `link.click()`).
- Remove the old plain-text key-reveal UI/logic from `/signup` entirely (replaced, not kept alongside).
- Verify with Playwright end-to-end: drawing something and signing up with a fresh username succeeds, downloads a PNG, and creates a session-less account (no login yet — Login is next task); a repeat signup with the same username fails cleanly without creating a second account; confirm no raw uploaded image file exists anywhere on disk after the request (only the small derived avatar file does).

## Done

## Details

- This intentionally replaces (not adds to) Placeholder identity's signup — Login (next feature) does the same for the login side; once both land, the key-based flow is fully retired.
- Avatar derivation's cropping code lives here out of technical necessity (raw bytes are never persisted), but displaying the avatar anywhere is out of scope for this task.
