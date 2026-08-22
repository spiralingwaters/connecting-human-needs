# History

Completed features, moved out of `FeaturesList.md` once checked off — kept here for the record, not meant to be revisited routinely.

- [x] Site shape: what sections exist, how people move between them, where gift notes live, and how bots take part — decided and written down before code.
- [x] Project skeleton: server, database, and a single styled page that renders.
- [x] Placeholder identity: signup hands out a random key the user copies; pasting it back logs them in. A plain stand-in for the PNG login, never called security.
- [x] Public feed: post, read, and reply in the open.
- [x] Search: find stream posts by keyword. Tentative ranking plan (tiered by term match, newest-first within each tier) in SiteShape.md "Open for later tasks" — still not finalized.
- [x] Gift notes: write a note (what's offered, how to reach you), see it, pass it on.
- [x] Note passing: pass a note openly or quietly; the author is notified when it's redeemed, nobody else.
- [x] Profiles: show what a person has offered and passed along; never show what they've received.
- [x] Private messaging between people, and with bots.
- [x] Blocking: hide a blocked person's posts, profile, and gift wall from you, and stop their private messages to you — a personal filter, silent, never a platform-wide score or punishment.
- [x] Bot framework: personas with stable names, avatars, specialties, and small prompts.
- [x] Fact extraction: pull structured facts (city, offers, needs, channels used) from bot conversations into the database.
- [x] Overlap engine: plain database matching to find who has what someone else needs, and whether they're reachable to each other.
- [x] Coordinator bots: reach out with a concrete match and a concrete next step.
- [x] Welcome bot: explain the 9-out-of-10 culture and why this isn't money or barter.
- [x] Offsite routing: help a giver post somewhere real and point the receiver at it.
- [x] Privacy enforcement: bots read only bot conversations, and never repeat personal details between people.
- [x] Doodle canvas: template with a dotted name line and a face square, a few colors, an eraser, and a clear button.
- [x] ID export: render the canvas to a high-resolution PNG the user downloads.
- [x] Signup: claim a unique username, check the image hash is unique, then release the PNG.
- [x] Avatar derivation: crop the face square down to a small clean avatar and store it.
- [x] Login: upload the PNG, hash it, match it, start a session.
