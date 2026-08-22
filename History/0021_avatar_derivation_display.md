# Feature Summary

- [ ] Avatar derivation: crop the face square down to a small clean avatar and store it.

## Description

Signup already derives and saves a small avatar file (`build/static/avatars/<user_id>.png`, a 96×96 crop of the face-square region) as a technical necessity of never persisting the raw uploaded image — but nothing displays it anywhere yet, matching SiteShape.md's note that avatar display was "deferred until the PNG identity feature lands." That feature has now landed, so this task's job is specifically the display wiring: show the avatar on `/u/<username>` (profile header, next to the username) and in the stream/thread views next to a post/message author's name, falling back to a plain placeholder circle for accounts with no avatar file (bots, and any account created before this feature existed).

- `/u/<username>`: show the avatar image (if `build/static/avatars/<id>.png` exists) beside the username in the profile header; a plain gray circle placeholder otherwise.
- Stream (`index.html`) and thread (`thread.html`): show a small avatar thumbnail next to each post/message's author name, same fallback rule.
- No new DB column needed — avatar presence is just "does `static/avatars/<id>.png` exist," checked at render time (a user's `id` is already available everywhere a template needs this).
- Keep this presentational only: no new route, no re-cropping logic (that's already correct from Signup) — just `<img>` tags with a sensible fallback.

## To Do

## Done

- Added `avatar_url(username)` as a Jinja global (looks up the user id, checks `static/avatars/<id>.png` existence) usable across profile/index/thread without duplicating the check in every route.
- Added the avatar `<img>` (or placeholder circle) to `profile.html`'s header, `index.html`'s per-post meta line, and `thread.html`'s per-message meta line.
- Styled the avatar (small circle, consistent sizes) and the placeholder fallback.
- Verified with Playwright: a freshly signed-up user's avatar renders as a real `<img>` correctly cropped on their own profile page and next to their post in the stream; the seeded bot (no avatar file) shows the placeholder `<span>` instead of a broken image — also confirmed visually with a screenshot.

## Details

- This task is purely about display — the actual cropping/storage already happened in Signup, out of necessity (the raw image can't be kept around to derive from later).
