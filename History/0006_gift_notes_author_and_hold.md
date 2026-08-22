# Feature Summary

- [ ] Gift notes: write a note (what's offered, how to reach you), see it, pass it on.

## Description

Build the gift note object itself and the first two steps of its lifecycle from SiteShape.md ("Gift note lifecycle"): **Authored** and **Held**. A gift note has a title, description, and contact info, an original author, a current holder, and an expiration date (30-day maximum, per SiteShape.md). Authoring a note requires being logged in (Placeholder identity) and sends it as a private message to one specific person — but Private messaging doesn't exist as its own feature yet, so this task builds the minimum private hand-off a note needs (recipient chosen by username at authoring time, note lands directly in their held list) without building the general messaging inbox/threads UI; that's explicitly deferred to the Private messaging feature. Passing a note on (from the current holder to a new person) and redeeming it are also part of the full lifecycle in SiteShape.md, but this task is scoped to authoring + holding + viewing only, per its FeaturesList.md wording ("write a note... see it, pass it on" — passing lands in the next task, Note passing, which also covers the redemption/public-announcement step). This task therefore stops at: author a note to a specific recipient, and the recipient can see it in their held list.

- DB: `gift_notes` table — id, title, description, contact_info, original_author_id, current_holder_id, expires_at, created_at.
- `/notes/new` — GET shows a form (title, description, contact info, recipient username, expiration handled automatically as +30 days from creation); POST validates the recipient exists, creates the note with current_holder_id = recipient, redirects to `/notes`.
- `/notes` — a logged-in user's held notes list: shows every gift_note where current_holder_id = them and not expired, each showing title, description, contact info, original author's username, and days until expiration.
- Expired notes (`expires_at` in the past) don't show in `/notes` — silently drop off per SiteShape.md ("quietly stops being redeemable/passable"), no separate cleanup job needed since the query itself filters on expiry.
- Authoring and viewing require a session (login); `/notes/new` and `/notes` redirect to `/login` if logged out.
- Out of scope this task: passing a note on to someone else, redeeming, the public redeemed-announcement post, renewal — all explicitly Note passing's job next.

## To Do

## Done

- Added `gift_notes` table to schema.sql.
- Added `/notes/new` route + template: author a note to a chosen recipient (by username), 30-day expiration set automatically.
- Added `/notes` route + template: logged-in user's held notes, unexpired only, showing original author + expiration.
- Required login for both routes (redirect to `/login` if logged out), same pattern as `/new`.
- Added a "My notes" header link, shown only when logged in.
- Styled the notes list/form consistently with existing forms/posts.
- Verified with a scripted test-client run: authoring a note to a valid recipient creates it and it shows in the recipient's `/notes` (not the author's own), authoring to a nonexistent username fails cleanly, an expired note (backdated in the test) does not show in `/notes`, logged-out access to both routes redirects to `/login`.

## Details

- Scoped deliberately short of full lifecycle — passing/redeeming/public announcement is FeaturesList.md's next item, Note passing.
- The "send to one specific person" step is a minimal stand-in for the general private-message compose action described in SiteShape.md ("sending a gift note is an action inside a person-thread") — full messaging UI is its own later feature.
