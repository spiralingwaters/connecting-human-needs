# Feature Summary

- [ ] Bot framework: personas with stable names, avatars, specialties, and small prompts.

## Description

Build the structural home for bot personas: stable named identities with a specialty tag and a short prompt, stored in the database (per Mission.md: "the database is the memory, not the context window"). This task builds personas as data plus the plumbing to let them act (post to the stream, hold/route notes, message people) — it does **not** wire up a live LLM call. Storing a persona's "prompt" is exactly what Mission.md describes regardless of how replies eventually get generated, so this doesn't need to wait on an infrastructure decision (self-hosted model vs. an API) — that decision only matters once a bot needs to generate free-form natural-language text, which the later features (Welcome bot, Coordinator bots) can each address with a simple templated stand-in for now, same pattern already used for Placeholder identity and the notifications stand-in elsewhere in this project. A bot is a real row in `users` (so it can author posts, hold gift notes, and appear in `/messages` and `/u/<username>` like anyone else) flagged `is_bot`, plus a `bot_personas` row carrying the specialty and prompt. Bots never sign up through `/signup` — they're seeded directly (a small seed script/data), since there's no PNG/key-issuance ceremony for a persona.

- DB: `users` gets an `is_bot` column (default 0). New `bot_personas` table: user_id (→ users.id), specialty, prompt (short text), created_at.
- A seed mechanism (extend `seed.sql` or a small Python seed function) creates 1-2 starter bot personas — enough to prove the framework works, not the full roster (that's later features' job to populate more as they need specific bots).
- `/u/<username>` for a bot-flagged user shows a small "bot" label next to the username (plurality/transparency: "openly bots," never disguised) — otherwise the profile page works unmodified (gift wall + own posts, same as any user).
- `/messages` already splits People/Bots by `is_bot_thread` on the thread — update thread creation so starting/finding a thread with a bot-flagged user automatically sets `is_bot_thread`, replacing the always-empty stub from Private messaging.
- No auto-reply logic yet — a message sent to a bot just sits there, same as a person who hasn't answered yet. That is explicitly fine and not a bug: the *conversational* behavior is scoped to the later Welcome bot / Coordinator bots tasks, using templates rather than a live model call.

## To Do

- Add `is_bot` column to `users`, `bot_personas` table to schema.sql.
- Seed 1-2 starter bot persona rows (user + bot_personas), e.g. a general-purpose "Circulator" bot, in seed.sql or an init helper.
- Update `find_or_create_thread`/thread creation to set `is_bot_thread` correctly based on whether either participant `is_bot`.
- Show a "bot" label on `/u/<username>` when that user is bot-flagged.
- Verify with a scripted test-client run: a seeded bot appears correctly labeled on its profile, starting a thread with a bot lands it in the Bots section of `/messages` (not People), a thread between two humans still lands in People.

## Done

## Details

- No live LLM integration in this task — that's a later decision, made when a feature actually needs generated natural language (Welcome bot, Coordinator bots), and can start as a template stand-in even then.
- Bots don't go through `/signup`/`/login` — they're seeded rows, not accounts anyone logs into.
