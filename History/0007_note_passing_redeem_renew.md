# Feature Summary

- [ ] Note passing: pass a note openly or quietly; the author is notified when it's redeemed, nobody else.

## Description

Finish the gift note lifecycle SiteShape.md laid out (steps 3-5: Passed, Redeemed, Expired-renewal), building on the Authored/Held steps the previous task built. From a held note, the current holder can either **pass** it on to someone else by username (removing it from their own held list, adding it to the next person's, still carrying the original author's name — same mechanic as authoring, just re-targeting an existing note instead of creating a new one) or **redeem** it (self-reported, one click). Redeeming is the *only* moment a note becomes public: it posts a single stream entry showing the note's title, the original author's username, and the redemption timestamp — reusing the existing `posts` table with a `kind` marker so the stream can tell a redemption post apart from a plain post (needed next for the shading distinction SiteShape.md describes, even though shading itself isn't built yet). Redemption also notifies the original author — "the author is notified when it's redeemed, nobody else" — and since private messaging doesn't exist yet, this task's stand-in for notification is a simple per-user notifications list surfaced in the header (a count/badge + a `/notifications` page), the same kind of minimal stand-in the Gift notes task used for "send to one person." Expired notes already silently drop out of `/notes` (previous task); this task adds the one-click **renew** SiteShape.md describes — re-authoring the same note (same title/description/contact/recipient... actually same original author, prompts for a fresh recipient since the old one no longer holds it) to send again.

- DB: `posts` gets a `kind` column (`'post'` default, or `'redemption'`); gift_notes gets no new columns — passing just updates `current_holder_id`, redeeming needs a `redeemed_at` marker so it can't be double-redeemed/passed after redemption, so add `redeemed_at` (nullable) to `gift_notes`.
- DB: `notifications` table — id, user_id, message, created_at, read (bool) — a minimal stand-in for the eventual private-message-based notification, same spirit as Gift notes' recipient-by-username stand-in for full messaging.
- `/notes/<id>/pass` — POST, current holder only, re-targets `current_holder_id` to a new username; 404/403 if not the current holder or already redeemed.
- `/notes/<id>/redeem` — POST, current holder only; sets `redeemed_at`, inserts a `kind='redemption'` post, inserts a notification for the original author. Once redeemed, note drops out of anyone's held list (query should exclude redeemed notes same as expired ones).
- `/notes/<id>/renew` — POST, original author only, on an expired note; creates a fresh gift_note with a new 30-day expiration to a newly-chosen recipient, same title/description/contact_info.
- `/notifications` — logged-in user's notifications, newest first, marks them read on view.
- Stream (`index.html`) distinguishes `kind='redemption'` posts visually (a distinct class, not yet real shading — SiteShape.md's green shading is still future work once distance/proximity exists) and their text is just "title — by original_author — redeemed" style, not a generic post body.
- Header shows an unread-notifications indicator when logged in.

## To Do

## Done

- Added `kind` column to `posts`, `redeemed_at` column to `gift_notes`, and a `notifications` table to schema.sql.
- Added `/notes/<id>/pass` route: validates holder + not redeemed, updates current_holder_id to new recipient.
- Added `/notes/<id>/redeem` route: validates holder + not redeemed, sets redeemed_at, inserts redemption post, inserts notification for original author.
- Excluded redeemed notes from the `/notes` held-list query (alongside the existing expiry filter).
- Added `/notes/<id>/renew` route: original-author-only, only for an expired note, prompts a new recipient, creates a fresh note.
- Added `/notifications` route + template; marks viewed notifications read; header shows an unread count.
- Updated `notes.html` to show Pass / Redeem forms per held note, and a Renew section for the author's own expired notes.
- Updated `index.html` to render `kind='redemption'` posts distinctly from plain posts.
- Verified with a scripted test-client run: pass moves a note from one holder's list to another's, redeem posts a public stream entry with the right text and removes the note from the holder's list, redeeming twice is a no-op (no duplicate announcement), a non-holder's pass/redeem attempts are no-ops, the original author (and only the original author) gets a notification on redemption, renew on an expired note creates a fresh 30-day note to a new recipient.

## Details

- Notifications here are a minimal stand-in (like Gift notes' recipient-by-username), not the real Private messaging feature — replace/fold in when that feature lands.
- Redemption post text and the green-shading distinction are separate concerns: this task only needs the `kind` marker and a CSS class; actual proximity-based shading depends on location data that still doesn't exist (per SiteShape.md, deferred since Public feed).
- "Passed" carries the *original* author's name forward, never the passer's — already modeled correctly since `original_author_id` never changes on pass, only `current_holder_id`.
