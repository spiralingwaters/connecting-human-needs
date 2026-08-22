# Feature Summary

- [ ] Profiles: show what a person has offered and passed along; never show what they've received.

## Description

Build the public profile page from SiteShape.md ("Profiles"): every profile is public and reachable by clicking a username. It shows the username, a **gift wall** (chronological list of that person's notes that have been redeemed — i.e. gift_notes where `original_author_id` = them and `redeemed_at IS NOT NULL`), and a chronological list of their own posts to the stream (plain posts they authored, `posts.author_id` = them, excluding redemption posts since those aren't "their" post, they're a note's — same distinction index.html already draws by `kind`). Avatar is explicitly deferred (SiteShape.md: "avatar (deferred until the PNG identity feature lands)") — no image placeholder needed beyond maybe a plain circle, keep it simple. No commenting/posting on someone else's profile — read-only, per SiteShape.md. This task also makes usernames clickable everywhere they already appear (post author names, gift note "from X", notification text stays plain since it's private) so `/u/<username>` is actually reachable.

- `/u/<username>` — public route, no login required (read access is universally open per Mission/SiteShape). 404-equivalent (simple "no such user" message) for an unknown username.
- Gift wall section: title, redemption date, for every gift_note where this user is `original_author_id` and `redeemed_at` is set — newest redeemed first.
- Posts section: this user's own plain posts (`kind='post'`), newest first — same post markup as the stream.
- Never displays anything about notes they've received/held/passed — only what they've *given* (redeemed as original author) and *said* (posted), per Mission.md "Giving is visible, receiving is private."
- Make `post.author_name` in the stream (`index.html`) and `note.original_author` in notes/redemption text link to `/u/<username>` where a username is available.

## To Do

## Done

- Added `/u/<username>` route + `profile.html` template: username header, gift wall (redeemed notes authored by them), their own plain posts.
- Handled unknown username with a plain "no such user" message, no crash.
- Linked post author names in `index.html` to `/u/<username>`.
- Linked the redemption post's "originally offered by X" text, and each held note's "from X", to profiles too.
- Styled the profile page consistent with existing pages.
- Verified with a scripted test-client run: a user's redeemed-as-author notes and plain posts show on their profile, a note they merely hold/redeemed (not authored) never appears on their own profile, an unknown username renders a clean "no such user" message, profile is reachable without being logged in.

## Details

- Avatar is explicitly out of scope (deferred to the PNG identity feature per SiteShape.md) — don't build a placeholder image system now.
- "Receiving is private" (Mission.md) — this is the one rule most worth re-checking carefully: a profile must never leak what notes someone is currently holding or has redeemed as a *holder* (only as the *original author* of a note that got redeemed does it show, and even then only title + date, matching the public redemption post's own visibility).
