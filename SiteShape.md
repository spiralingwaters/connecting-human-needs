# Site Shape

The output of the "Site shape" feature: what the site is, section by section, and how a gift note and a bot move through it. Every later feature builds against this rather than re-deciding layout.

## What the site is

One flat, chronological stream — chatroom-shaped, not a message board with threads. Gift notes are one kind of post inside it, not a separate section. There is no "notes area" and no "chat area"; there is one timeline everyone posts into.

## Landing page

The Global stream, unauthenticated, read-only. This is the whole site for a logged-out visitor — no separate marketing page, no explainer wall. A **Local** toggle filters the same stream to nearby posts by time; both views are the same timeline, just filtered.

## The stream

- Every post is a peer: a plain message, a redeemed-note announcement, or a bot-originated post (welcome, a match made, a weekly circulation digest). Gift notes themselves are never posted publicly while active — see Gift note lifecycle below.
- No nested replies, no comment threads. `@username` refers to someone inline — a link, not a thread.
- **Proximity shading**: every ordinary post's background is shaded by rough distance between the viewer's location and the post author's — same city near-white, nearby very light, far away darker gray. Rough lat/lon comes from a logged-in user's signup city/zip, and from a best-guess (IP-based) location for a visitor who isn't logged in at all, so shading works from the first page load. The exact distance (down to about half a mile) is computed **client-side**, in the browser, from the two raw rough lat/lon numbers the server sends down — the server never has to compute distance for every viewer/post pair itself. The underlying points are city/zip-scale, not addresses, so the number is precise given rough inputs, not GPS-precise.
- Posting requires an account (placeholder-identity key). Reading does not.

## Profiles

Every profile is public and reachable by clicking a username anywhere. A profile shows: username, avatar (deferred until the PNG identity feature lands), a **gift wall** (the chronological list of that person's notes that have been redeemed), and a chronological list of their own posts to the stream — so an `@mention` ("@username is trying to redeem all my gift notes") can be clicked through to see what they've actually said or what they were responding to. No one can post *on* another person's profile — it's a read-only view of things they've already said or given elsewhere; the only person-to-person contact off the shared stream is a private message.

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

A gift note is never posted to the public stream while active — discovery happens the ordinary way, through spoken needs in the flat stream or in conversation, and a giver who sees an overlap decides who to send to. The note itself only surfaces publicly once, at the very end.

1. **Authored** — the giver writes a note (title, description, contact info) and sends it as a **private message to one specific person they choose**. An expiration date is set (site enforces a 30-day maximum). Nothing about this step is public.
2. **Held** — the note lands in the recipient's own **held notes** list on the site (visible only to them). It always displays the **original author's** username, for as long as it's held, however many hands it's passed through — which is also how someone can notice "I keep receiving notes that trace back to the same person" without the platform ever tallying or scoring that. If a note is instead handed over entirely off-site (in person, no message sent through the platform), the site never knows and never needs to.
3. **Passed** — from their held list, the holder can send it on to someone else with one action (a private message again, removing it from their list and adding it to the next person's), still carrying the original author's name.
4. **Redeemed** — the current holder clicks "redeemed" from their held list. This is self-reported and optional; the site is a courtesy layer, never the source of truth. This is the **one and only moment** the note becomes public: a single stream post appears, showing just the note's title, the original author's username (linked), and the redemption timestamp — no commentary, and no mention of when it was first offered or who redeemed it. It's added to the original author's gift wall at the same time. Clicking redeem is itself a small gift twice over — it hands the giver a new gift-wall entry, and it shows the whole site that a gift moved.
5. **Expired** — if unredeemed past its date while still someone's held note, it quietly stops being redeemable/passable and drops off that person's held list; since it was never public, there's nothing to visibly "fail." The original author gets a one-click **renew** — re-authoring the same note to send again — covering the "gives the same thing away every few days" case without a separate recurring-gift mechanism.

### Redeemed announcements

- Shaded a **subtle green**, not far off white, instead of the ordinary gray proximity shading — a redeemed post is visually distinct from an active conversation post. The distance number/km to the original author is still shown as text, same as any other post; only the background stops following the gray distance gradient.
- **Always shown in both Global and Local streams**, regardless of which view the person has open — a completed gift is worth surfacing everywhere, not filtered out because the giver was far away. This isn't a "new site" bootstrapping rule; it stays permanent, since it's exactly the cross-distance visibility ("many people being generous, anywhere to anywhere") the Mission is trying to make normal.

## Bots in the open

Bots post their own content — never replies, never threaded under a human's post. Plurality (many visible personas) comes from bots authoring their own posts (welcome messages, match announcements, a circulation digest), not from commenting on everyone else's.

## Bot-held notes and routing

A bot can receive a note but can never redeem one. Instead it looks for who to route it to next:

- Ranks candidates using only already-public signal — a person's own visible gift-wall history (are they someone who circulates things) — the same thing a human could see by browsing profiles. Never a hidden score.
- Weighs candidates near the **original giver** using the same proximity system as the stream shading, so redemption doesn't require crossing the country.
- Only ever orders candidates for outreach; never excludes anyone or gates access.
- Reaches out by private message, and says plainly that it's routing this on the original giver's behalf — no staged coincidences.

## Bots offering things they found

A bot can also go looking for free things elsewhere (a free-listings site, a local group) and match them against known needs or interests on this site — then send a gift note itself, as its own persona, the same as a human would. Redeeming it doesn't hand over anything the bot holds; it reveals the real external location or link. This has to stay honest to survive being found out: the note is framed as "I found this, here's where it is" from the start, never as if the bot personally possesses the thing.

## Rough page map

- `/` — Global stream (landing page; Local toggle filters it)
- `/u/<username>` — public profile: posts + gift wall
- `/notes` — your held gift notes (private to you): pass on or redeem
- `/messages` — private messages, split into person threads and bot threads; sending a gift note is an action inside a person-thread, not a public compose
- `/new` — compose a plain post to the stream (never a gift note)
- `/signup`, `/login` — placeholder-identity key issuance and re-entry

## Open for later tasks

- Exact wording/visuals for the gray proximity-shade scale and the green redeemed shade.
- Exact wording for the compose-a-gift-note action inside a message thread.
- **Blocking only protects the blocker** — a slur is still visible to everyone who hasn't blocked that person. Whether the site also needs real moderation (reporting, and someone or something with authority to remove a post platform-wide) is a separate, bigger decision — there's no admin/moderator role defined anywhere yet — and is still open.
- **Search ranking vs. the always-newest-first stream is unresolved.** The stream itself is meant to always show newest-first, no exceptions — but search was pitched as tiered (all search terms match first, then some terms, then one term), which is a relevance ordering, not a time ordering. Whether search results keep newest-first within each relevance tier, ignore relevance and just filter+sort by time, or do something else entirely is not decided. Settle this before building Search.
