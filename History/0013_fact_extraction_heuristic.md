# Feature Summary

- [ ] Fact extraction: pull structured facts (city, offers, needs, channels used) from bot conversations into the database.

## Description

Build the structured-facts store bot conversations feed into, per Mission.md ("the database is the memory, not the context window... personas load a handful of structured facts"). Real extraction eventually needs language understanding, but no LLM is wired up yet (deliberate scope decision carried from Bot framework/Welcome bot). This task builds the honest, currently-available version: a simple rule-based extractor (keyword/regex patterns) that scans a human's messages *sent to a bot thread* (never human-to-human threads — Mission.md's hard privacy rule) for a few recognizable shapes: "I have/offer <thing>", "I need/looking for <thing>", "I'm in <city>", and a contact channel mention (an email-looking string, or "reach me on X"). This is clearly a heuristic stand-in, documented as such, matching this project's established pattern (Placeholder identity, notifications, Bot framework's templated replies) of building a working simple version now and swapping in the real thing later without needing to redesign the schema.

- DB: `user_facts` table — id, user_id, key (`'city'`, `'offers'`, `'needs'`, `'channel'`), value (free text), source_thread_id (→ message_threads), created_at. A user can have multiple facts of the same key (e.g. several separate offers).
- Extraction runs at the moment a message is inserted into a **bot thread** by the human side (in `thread()`'s POST handler, only when `message_threads.is_bot_thread` is true and the sender isn't the bot) — simple pattern matching against the message body, inserting any facts it recognizes. No batch job, no background worker — KISS, extraction happens inline with the request that creates the message.
- Never runs against person-to-person threads — enforced by checking `is_bot_thread` before extracting, matching Mission.md's "bots never read human-to-human conversations."
- No UI surface required for this task beyond what's needed to verify it worked (facts existing in the DB) — Overlap engine (next) is what actually reads and uses `user_facts`.
- Out of scope: any real NLP/LLM-based extraction — flagged as a known simplification to revisit once an LLM decision is made (see Bot framework's Details).

## To Do

## Done

- Added `user_facts` table to schema.sql.
- Added `extract_facts(body)`: regex/keyword rules for offers, needs, city, channel — returns a list of (key, value) pairs found.
- Wired it into `thread()`'s POST handler: runs only when the thread `is_bot_thread`, inserting any facts found tagged with `source_thread_id`.
- Verified with a scripted test-client run: a message with offer/city/channel shapes produces the expected facts in a bot thread, the identical message in a human-to-human thread produces none, and ordinary chat with no recognizable shape produces no false positives.

## Details

- Heuristic, not real NLP — a known, documented simplification (same category as Search's plain-LIKE ranking and Bot framework's no-LLM-yet choice). Revisit once a real language model is wired in.
- Enforcing "bot threads only" here is also the first concrete piece of the later Privacy enforcement feature, though that feature will need to audit this more thoroughly across the whole app, not just this one insertion point.
