# Feature Summary

- [ ] Private messaging between people, and with bots.

## Description

Build the real messaging surface SiteShape.md describes: two structurally different channels — person-to-person threads (never read by any bot) and person-to-bot threads (where coordinator bots do their matching work) — visible as separate surfaces, not one inbox. Bot framework/personas don't exist yet (later FeaturesList.md items), so the person-to-bot side of this task is scoped to the plumbing only: a thread *can* be addressed to a bot-flagged user row, and the interface keeps it in its own list, but no bot ever actually replies yet (that's Bot framework's job). This task also retrofits Gift notes' "send to one person" and Note passing's "pass to one person" — currently plain form fields with no visible history — into real message threads: authoring/passing a note becomes an action inside a person-thread (per SiteShape.md: "sending a gift note is an action inside a person-thread, not a public compose"), rather than duplicating a separate ad-hoc mechanism. The existing `notifications` stand-in from Note passing (redemption pings the original author) stays as-is — that's a system notice, not a conversation, and SiteShape.md doesn't describe redemption notices as messages.

- DB: `message_threads` table (id, user_a_id, user_b_id, is_bot_thread, created_at) and `messages` table (id, thread_id, sender_id, body, created_at). A thread is uniquely keyed by its two participants (person-to-person) — reuse an existing thread rather than creating duplicates.
- `/messages` — logged-in user's thread list, split into two sections: "People" and "Bots" (per SiteShape.md's visible split), each showing the other participant + a preview of the latest message.
- `/messages/<thread_id>` — the thread view: full message history, a compose box to send a new message, and (only inside a person-thread, matching SiteShape.md) a "Send a gift note" action that opens the same form Gift notes already built, posting the resulting note as a message in this thread instead of firing off separately.
- `/messages/new` — start a thread with a username (person) — since no bot personas exist yet, this task only supports person threads; the "Bots" section of `/messages` stays empty until Bot framework lands, which is fine and expected, not a gap to fake-fill.
- Retrofit `/notes/new`: instead of a bare form posting directly, `recipient` selection becomes "open/start a thread with this username first" — simplest correct approach: keep the same route and form (still asks for a recipient username directly, since there's no thread-picker UI elsewhere yet) but internally: find-or-create the person-thread with that recipient, then insert both a `messages` row (so it shows in the thread) and the `gift_notes` row. Passing a note (`/notes/<id>/pass`) does the same against the new holder.
- Only the two participants of a thread may ever see it or post to it; a bot-thread never shows to anyone but the human side (bots don't have their own login yet, so nothing else to guard).

## To Do

## Done

- Added `message_threads` and `messages` tables to schema.sql.
- Added a `find_or_create_thread` helper between two user ids.
- Added `/messages` route + template: split People / Bots sections (Bots empty until Bot framework exists).
- Added `/messages/<thread_id>` route + template: history + compose box; guarded so only participants can view/post.
- Added `/messages/new` route + template: start a thread by username.
- Retrofitted `/notes/new` and `/notes/<id>/pass` to drop a message into the relevant person-thread alongside creating/moving the gift note.
- Added a header nav link to `/messages`.
- Verified with a scripted test-client run: starting a thread and sending messages works, a third user is redirected away from someone else's thread, authoring a gift note creates/reuses a thread with a message in it, passing a note does the same with the new holder, starting a thread with the same person twice reuses the one thread.

## Details

- Bot side is plumbing-only this task — `is_bot_thread` exists in the schema and the UI has a labeled empty section for it, but no bot persona or auto-reply exists until Bot framework (FeaturesList.md, later).
- Redemption notifications (Note passing's `notifications` table) are intentionally left alone — they're a system notice, not a conversation between two people, so they don't get folded into `messages`.
