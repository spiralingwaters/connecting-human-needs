# Feature Summary

- [ ] Public feed: post, read, and reply in the open.

## Description

Build the flat, chronological stream from SiteShape.md: one column, newest-to-oldest, no nested replies (an `@username` is just inline text for now — profile links don't exist until the Profiles feature). Reading works for anyone. Posting normally requires an account (SiteShape.md), but Placeholder identity hasn't been built yet — picked out of FeaturesList.md order via the dashboard's "work on next" flag, so this task scopes around that gap rather than blocking on it: posting uses a plain, clearly-temporary "poster name" text field with no session, no account, no security of any kind — not a preview of the real identity system, just the minimum needed to see posts flow. It gets ripped out and replaced with real accounts when Placeholder identity lands. Proximity shading (gray-by-distance, green for redeemed) is out of scope here too — it needs signup city/zip or IP geolocation, neither of which exist yet — so posts render with a single neutral background for now.

- DB: `posts` table — id, author_name, body, created_at.
- `/` (already exists) — list posts newest-first, plain single column, neutral background per post (no proximity shading yet).
- `/new` — GET shows a compose form (poster name + message body), POST inserts a row and redirects to `/`.
- No reply threading, no nested comments — matches SiteShape.md.
- No proximity shading, no Local toggle filtering yet — needs location data that doesn't exist until identity/geolocation land; flagged as follow-up, not silently dropped.
- Posting is deliberately not gated by any account — temporary, to be replaced wholesale once Placeholder identity exists.

## To Do

## Done

- Added `posts` table to schema.sql + a seed post.
- Updated `/` route + template to list posts newest-first.
- Added `/new` route (GET form, POST insert) + template.
- Added styling for the stream, compose link, and compose form.
- Verified with a scripted test-client run: seed post renders, `/new` form loads, posting inserts and redirects, new post appears before the seed post (newest-first), empty submissions are rejected without creating a post.

## Details

- Picked via dashboard "work on next" flag, ahead of Placeholder identity in FeaturesList.md order — deliberate, not an oversight.
- Posting today has zero auth/security — must be swapped for real accounts when Placeholder identity is built (schema will need an author reference at that point, not just a free-text name).
- Proximity shading and the Local toggle are explicitly deferred — they depend on location data this task doesn't have.
