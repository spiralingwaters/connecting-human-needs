# Feature Summary

Site shape: what sections exist, how people move between them, where gift notes live, and how bots take part — decided and written down before code.

## Description

Before any server exists, decide the actual shape of the site: what a person sees when they arrive, what sections there are, how they move between them, where a gift note lives at each moment of its life, and how bot personas take part in the open versus in private. The Mission constrains this more than it first appears. Offers are codified and requests are only spoken, so needs must live in ordinary conversation and must never become a form, a list, a queue, or anything countable — that rules out a "needs board" no matter how convenient it looks. Giving is visible and receiving is private, so a profile can render an offer history but must have no place a receipt could ever be displayed. Bots may read bot conversations only, so human-to-human messages and human-to-bot messages are structurally different channels, not one inbox with a filter. And leaving is a success, so the design should make it easy to finish and close the tab rather than rewarding another scroll. The output of this task is a written structure document plus a rough page map — no code, no database, no styling decisions beyond layout. Every later feature reads from it.

- Decide the primary surface: the first thing a logged-in person sees, and what the site "is" in one sentence.
- Decide where gift notes live: inline in the public stream as a distinct post type, or their own browsable section, or both.
- Decide where a held note sits between being received and being passed on (a pocket, a profile shelf, nowhere).
- Decide how bots appear in the open: posting alongside humans in the same stream, or only reaching out privately.
- Decide how the two private channels differ in the interface: human-to-human versus human-to-bot, given bots may only read the latter.
- Decide what a logged-out visitor sees first: the live site, or an explanation of why it works this way.
- Keep the section count as low as it can go — KISS applies to the site map before it applies to any code.
- Write the result into a structure document in the repo, with a page map, so every later feature builds against it.

## To Do

- Get the user's read on `SiteShape.md` as a whole — anything to change before this task is marked done.

## Done

- Answered the open structural questions with the user (primary surface, where notes live, how bots appear, what a visitor sees first, blocking).
- Drafted the page map: every section, what it holds, and every link between sections.
- Walked a gift note's whole life through the map — authored, held, redeemed, expired/renewed — confirmed each step has a place to happen.
- Confirmed needs stay purely conversational: no needs board, no queue, nothing countable anywhere in the map.
- Checked the map against the hard privacy rules: no surface displays a receipt; bot/human message channels are structurally separate; bot-held notes are the only custody the site tracks.
- Wrote `SiteShape.md` into the repo and linked it from Mission.md's "More" section.
- Reviewed the map for simplicity: one flat stream instead of separate sections for notes/chat; no nested comment threads.
- Added the Blocking feature (raised mid-task) to `FeaturesList.md` and to `SiteShape.md`.

## Details

- Mission constraints that bind this task: offers codified / requests only spoken; giving visible / receiving private; bots read bot conversations only; notes pass openly or quietly; leaving is a success, not churn.
- No code, no schema, no stack decisions in this task — the stack question stays open on the dashboard.
- `SiteShape.md` is the artifact this task produced; later features are built against it rather than re-deciding layout.
- Real-content moderation (reporting/removal, beyond personal blocking) is flagged as open in Mission.md's "Need to Revisit" — no admin role exists yet, and it wasn't decided in this task.
