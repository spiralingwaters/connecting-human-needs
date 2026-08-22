# Feature Summary

- [ ] Welcome bot: explain the 9-out-of-10 culture and why this isn't money or barter.

## Description

Give the seeded "circulator" persona (from Bot framework) its first real behavior: greet a brand-new user. Per Mission.md ("small roles, short prompts... Honest about being coordinated"), this is templated text for now, not a live LLM call — the bot's stored `prompt` field describes its voice for whenever generation is wired up later, but the actual message text here is a fixed, well-written explanation of the culture, sent the same way any bot-to-person contact happens: a private message thread (Private messaging feature), landing in the new user's Bots section. This keeps the behavior simple, honest, and testable without depending on external LLM infrastructure.

- On successful `/signup`, after the new user row is created, the circulator bot automatically starts a thread with them (via `find_or_create_thread`, already bot-thread-aware from Bot framework) and sends one message explaining: what circulates here (offers, not money), the pass-on-9-of-10 norm, that it's social not platform-enforced, and that giving is visible while receiving stays private.
- This uses the existing `messages` table exactly as a human-to-person message would — no new schema needed.
- If no bot persona exists (shouldn't happen since one is seeded, but keep it defensive), signup should not fail — skip the welcome message rather than erroring.
- Out of scope: any dynamic/personalized content in the welcome message (that's a live-LLM-generation concern for later); this is one fixed, good message.

## To Do

## Done

- Added the welcome-message send to `/signup`'s POST success path: find-or-creates a thread between the new user and a bot, inserts one message with the fixed welcome text.
- Guarded for no bot persona existing (defensive no-op — shouldn't trigger with the seed in place).
- Verified with a scripted test-client run: signing up a new user creates a bot thread with the welcome text already in it, visible in `/messages` and the thread view.

## Details

- Message content itself needs to read naturally and warmly, matching Mission.md's tone (not just a bullet dump) — write real prose for the welcome text, not a template needing per-user substitution.
- No live LLM call in this task, matching the same choice made in Bot framework.
