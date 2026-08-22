# Feature Summary

- [ ] Privacy enforcement: bots read only bot conversations, and never repeat personal details between people.

## Description

Every bot-touching code path built so far (Fact extraction, Overlap engine, Coordinator bots) already happens to respect these rules, but only because each was written carefully by hand — nothing centrally enforces or tests it as an invariant. This task makes the rule explicit in code (a single guarded entry point bot logic must go through) and adds a dedicated test suite that would catch a regression if a future feature accidentally reads a human-to-human thread or leaks more than it should. This is a hardening/audit task, not new user-facing behavior.

- Add a small guard function, `assert_bot_thread(t)`, that raises if called on a thread where `is_bot_thread` is false. Wire it into the two places that currently read thread content for bot purposes (fact extraction and coordinator follow-up in `thread()`'s POST handler) so the "only bot threads" rule is enforced by code, not just by the `if t["is_bot_thread"]:` branch already there — belt and suspenders, since the branch guard already exists but nothing stops a future call site from skipping it.
- Audit "never repeat personal details between people": check every bot-authored message text (Welcome bot's fixed text, Coordinator bots' follow-up) contains only (a) fixed copy, (b) the matched offer's own text (which its author chose to state as an offer — offers are meant to be public per Mission.md, "Offers are codified"), and (c) a username. Confirm nothing else about either party (their `needs` facts, their city, their other messages) ever appears in a bot-authored message headed to someone else. Document this as the specific check going forward for any future bot message template.
- Add a dedicated test file/script (not just inline in a Task like previous features) covering: a coordinator notice never contains the *searcher's* own need-text verbatim beyond what they already said themselves in their own thread (i.e., it isn't echoed to a third party), fact extraction never runs against a human-to-human thread even if crafted input looks bot-like, and `assert_bot_thread` actually raises when misused.

## To Do

- Add `assert_bot_thread(t)` and wire it into fact-extraction and coordinator-follow-up code paths in `thread()`.
- Write `build/test_privacy.py` (or similar) as a standalone scripted test file covering the invariants above, runnable via `python3 build/test_privacy.py` — first dedicated test file in the project (earlier features verified inline in the session, this one is worth keeping around to re-run).
- Verify with a scripted test-client run (via the new test file): human-to-human threads never produce facts or coordinator notices no matter what's said in them; `assert_bot_thread` raises on a non-bot thread; no bot-authored message content includes anything beyond fixed copy, a self-stated offer, or a username.

## Done

## Details

- This task doesn't change what already worked correctly — it adds enforcement and regression coverage for an invariant that held by construction, per the project's "build until it works, then check it actually serves the mission" step in Mission.md's How We Build.
- The dedicated test file (rather than inline scratch tests like earlier tasks) is deliberate here: privacy invariants are exactly the kind of thing worth guarding against silent regressions as more bot features get added later.
