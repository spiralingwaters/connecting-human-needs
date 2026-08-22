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

- Answer the open structural questions with the user (primary surface, where notes live, how bots appear, what a visitor sees first).
- Draft the page map: every section, what it holds, and every link between sections.
- Walk a gift note's whole life through the map — written, seen, passed openly, passed quietly, redeemed, author notified — and confirm each step has a place to happen.
- Walk a need's whole life through the map — spoken, noticed by a bot, matched, routed offsite — and confirm nothing turns it into a countable object.
- Check the map against the hard privacy rules: no surface can ever display a receipt, and no bot can reach a human-to-human message.
- Write the structure document into the repo and link it from Mission.md's More section.
- Review the map once more purely for simplicity: can any section be removed or merged?

## Done

## Details

- Mission constraints that bind this task: offers codified / requests only spoken; giving visible / receiving private; bots read bot conversations only; notes pass openly or quietly; leaving is a success, not churn.
- No code, no schema, no stack decisions in this task — the stack question stays open on the dashboard.
- The structure document is the artifact this task produces; later features are built against it rather than re-deciding layout.

- Decisions locked so far: one flat chronological stream (Global/Local view toggle, not separate sections), gift notes are a post type inside it, proximity-shaded post backgrounds from rough signup city/zip, 30-day expiration as an author-settable maximum with one-click renew, redemption is a self-reported optional click (site is a courtesy layer, never required), bots post their own content rather than replying/threading, @mentions instead of nested comments.
- Still open: what a logged-out visitor sees first; whether on-site "passing" needs any custody tracking or is just generating a shareable link/message.
