# Feature Summary

- [ ] Login: upload the PNG, hash it, match it, start a session.

## Description

Replace `/login`'s temporary "being rebuilt" stub (left in place during Signup) with the real flow: upload the PNG file you downloaded at signup, the server hashes the raw bytes the same way Signup did, looks for a matching `users.image_hash`, and starts a session on a match. This completes the identity chain and fully retires Placeholder identity's key-paste login — matching Mission.md's "no recovery, by design" property, since the uploaded file's hash either matches exactly or it doesn't (no partial credit, no password reset).

- `/login` GET: a plain file upload form (`<input type="file" accept="image/png">` + submit), replacing the old key-paste field and the "being rebuilt" placeholder message.
- `/login` POST: reads the uploaded file's raw bytes (never persisted, same rule as Signup), computes `sha256`, looks up `users` by `image_hash`; on a match, starts the session (`session["user_id"]`) and redirects to `/`; on no match, shows a plain "not recognized" error and lets the person retry (no partial state, no lockouts, no rate-limit theater — this is deliberately not real security per Mission.md/FeaturesList.md's own framing).
- No new schema — reuses the `image_hash` column Signup already added.

## To Do

## Done

- Rewrote `/login`'s template: a file upload form for the PNG, replacing the stub message and old key field.
- Rewrote `/login`'s POST handler: reads the uploaded file, hashes it, looks up by `image_hash`, starts the session on match or shows an error otherwise.
- Updated `build/test_privacy.py`'s `signup_and_login` helper to log in for real via `/login` (re-uploading the same PNG bytes) instead of the interim `session_transaction` shortcut.
- Verified with Playwright end-to-end: signed up a fresh account, downloaded the PNG, uploaded that exact file to `/login` and confirmed a session started (header shows "logged in as finn"); uploading an unrelated image was rejected cleanly with no session created.

## Details

- This is the last remaining feature in FeaturesList.md — once this lands, Placeholder identity's key-based flow is fully retired and the real PNG-drawing identity system (Doodle canvas → ID export → Signup → Avatar derivation → Login) is complete end to end.
- No password-reset-style recovery is added here, matching Mission.md's explicit "losing the PNG means losing the account permanently — no recovery, by design."
