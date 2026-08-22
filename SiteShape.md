# Site Shape

The output of the "Site shape" feature: what the site is, section by section, and how a gift note and a bot move through it. Every later feature builds against this rather than re-deciding layout.

## What the site is

One flat, chronological stream — chatroom-shaped, not a message board with threads. Gift notes are one kind of post inside it, not a separate section. There is no "notes area" and no "chat area"; there is one timeline everyone posts into.

## Landing page

The Global stream, unauthenticated, read-only. This is the whole site for a logged-out visitor — no separate marketing page, no explainer wall. A **Local** toggle filters the same stream to nearby posts by time; both views are the same timeline, just filtered.

## The stream

- Every post is a peer: a plain message, a gift note (offer), a bot-originated post (welcome, a match made, a weekly circulation digest), or an in-place update marking a note redeemed.
- No nested replies, no comment threads. `@username` refers to someone inline — a link, not a thread.
- **Proximity shading**: every post's background is shaded by rough distance between the viewer's signup city/zip and the post author's — same city near-white, nearby very light, far away darker gray. Computed per-viewer at render time from two rough lat/lon points; no exact location is ever stored per-post.
- Posting requires an account (placeholder-identity key). Reading does not.

## Profiles

Every profile is public and reachable by clicking a username anywhere. A profile shows: username, avatar (deferred until the PNG identity feature lands), and a **gift wall** — the chronological list of that person's notes that have been redeemed. Nothing else. No one can post on another person's profile; the only person-to-person contact off the shared stream is a private message.

## Private messages

Two structurally different channels, since bots may read bot conversations but never human-to-human ones:

- **Person-to-person messages** — never read by any bot.
- **Person-to-bot messages** — where coordinator bots do their matching work.

These are visibly different surfaces in the interface, not one inbox with a label, so the boundary is obvious from using the site rather than something you have to trust a policy about.

## Blocking

A personal filter, not a platform punishment — one person choosing not to see another, never enforced or scored by the site itself:

- Blocking someone hides their posts from your view of the stream, empties their profile and gift wall when you view it, and stops new private messages from them to you. Existing message history you already have stays.
- You still see **other people's** posts that `@mention` a blocked user — blocking only removes what *they* post, not what others say.
- Silent: the blocked person isn't told they've been blocked.

## Gift note lifecycle

1. **Authored** — posted to the stream as an active offer, with an expiration date the author sets (site enforces a 30-day maximum).
2. **Held** — by a human, this is invisible to the site; a note can be received and redeemed entirely off-platform, with nothing reported back. By a **bot**, this is the one case the site tracks explicitly (see below), since the bot needs somewhere to hold state while it looks for who to route the note to.
3. **Redeemed** — whoever currently holds the note clicks "redeemed." This is a self-reported, optional act; the site is a courtesy layer, never the source of truth. The click updates the original post in place (no duplicate stream clutter) and adds an entry to the **original author's** gift wall — never the holder's, never a bot's, and the redeemer is never named.
4. **Expired** — if unredeemed past its date, the post simply ages out of being claimable; it doesn't disappear from the stream (it's a chat log, not a listing) and carries no "failed" label. The author gets a one-click **renew**, covering the "gives the same thing away every few days" case without a separate recurring-gift mechanism.

## Bots in the open

Bots post their own content — never replies, never threaded under a human's post. Plurality (many visible personas) comes from bots authoring their own posts (welcome messages, match announcements, a circulation digest), not from commenting on everyone else's.

## Bot-held notes and routing

A bot can receive a note but can never redeem one. Instead it looks for who to route it to next:

- Ranks candidates using only already-public signal — a person's own visible gift-wall history (are they someone who circulates things) — the same thing a human could see by browsing profiles. Never a hidden score.
- Weighs candidates near the **original giver** using the same proximity system as the stream shading, so redemption doesn't require crossing the country.
- Only ever orders candidates for outreach; never excludes anyone or gates access.
- Reaches out by private message, and says plainly that it's routing this on the original giver's behalf — no staged coincidences.

## Rough page map

- `/` — Global stream (landing page; Local toggle filters it)
- `/u/<username>` — public profile + gift wall
- `/messages` — private messages, split into person threads and bot threads
- `/new` — compose a post (plain message or gift note)
- `/signup`, `/login` — placeholder-identity key issuance and re-entry

## Open for later tasks

- Exact wording/visuals for the proximity-shade scale and the redeemed-in-place post state.
- Whether the compose flow for a gift note differs visually from a plain message, or is one form with an "this is an offer" toggle.
- **Blocking only protects the blocker** — a slur is still visible to everyone who hasn't blocked that person. Whether the site also needs real moderation (reporting, and someone or something with authority to remove a post platform-wide) is a separate, bigger decision — there's no admin/moderator role defined anywhere yet — and is still open.
