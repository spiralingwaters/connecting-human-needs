# Feature Summary

- [ ] Coordinator bots: reach out with a concrete match and a concrete next step.

## Description

Close the loop the Overlap engine opened: instead of only showing candidates on a page someone has to check, a bot proactively messages a person when a concrete overlap exists, per Mission.md ("Honest about being coordinated... no staged coincidences — a bot says plainly 'someone here is giving away a couch in your city, here's the link'"). The message is templated text (not live-LLM-generated, consistent with every other bot behavior built so far) that plainly states what was matched and a concrete next step: go start a conversation with that person. This task triggers on the same event Fact extraction already hooks: right after a `needs` fact is extracted from a message in a bot thread, immediately run the Overlap engine for that user and, for any new match found, have the bot send a follow-up message in that same bot thread naming the match and linking to `/messages/new` (or directly proposes starting a thread with that username).

- No new schema for the match itself, but avoid re-notifying about the same pair repeatedly: add a small `coordinator_notices` table (user_id, matched_username, offer_value, created_at) recording what's already been surfaced, so the same offer isn't re-announced to the same person every time they send another message.
- After fact extraction inserts a `needs` fact, call `find_overlaps` for that user; for each match not already recorded in `coordinator_notices` (matched on user_id + matched_username + offer_value), have the bot post a message in the same bot thread: "Someone here is offering '<offer>' — that sounds like what you're after. Want to reach out? Start a conversation with @<username>." Then record it.
- This only fires from a *human* message being posted to a *bot thread* that yields a new `needs` fact and at least one match — never a background job, matching the project's inline/no-worker pattern established by Fact extraction.
- Out of scope: actually initiating a thread on the user's behalf (SiteShape.md keeps "reaches out" as the bot's own private message, but the actual person-to-person conversation still needs the human to choose to start it) — the bot's job is the concrete pointer, not doing the introduction on its own authority beyond that message.

## To Do

## Done

- Added `coordinator_notices` table to schema.sql.
- After fact extraction in `thread()`'s POST handler, when a new `needs` fact was recorded, runs `find_overlaps` and sends a follow-up bot message (in the same thread) for each match not already in `coordinator_notices`; records each one sent.
- Verified with a scripted test-client run: a matching need produces both the extracted fact and a coordinator follow-up naming the offering username, a repeat similar need doesn't re-send the same notice, an unmatched need produces no follow-up.

## Details

- Templated, not live-LLM-generated — same choice made throughout the bot features so far (Bot framework, Welcome bot).
- This task deliberately only fires on new `needs` facts, not new `offers` facts — matching the other direction (telling an existing offerer about a newly-arrived need) is a reasonable future enhancement but doubles the surface area and isn't required by the feature's wording ("reach out with a concrete match"), so it's left for later rather than silently expanded here.
