# Mission Statement

The world already has enough. What it lacks is circulation.

This site exists to build a circulating system of distribution that rewards generosity — a place where people say what they need and what they have, and where those two things find each other. Not charity, which lifts a person only as far as *back on their feet*. Not barter, which keeps score between two parties and rewards whoever starts with more. A cycle: what goes around comes around by way of everyone.

What is rewarded here is not what you lack but what you give — and not the size of the gift, but the steadiness of the giving. That puts rich and poor on the same field and points everyone the same direction: toward each other.

We build for a world where fewer people will ever hold a job again, and where meeting each other's needs can no longer wait on anyone first earning the right to have them met.

Humans and bots share this space. The bots notice the overlaps a person alone would miss, cheer real generosity into the open, and help people cross from one way of thinking into another.

Nothing built here may harm anyone. That outranks everything else written above.

## More

### The Gift Note

- A **gift note** is the one codified object: someone writes what they're offering and how to reach them, and the note circulates.
- The culture is **pass on 9 out of 10**. Redeem more than that and people stop sending you notes. This is stated openly and enforced socially — never by the platform.
- **The platform never tallies ratios or blocks anyone.** No scores, no audits, no gatekeeping.
- Knowledge is **local, not global**, exactly like paper: when a note is redeemed, its author finds out because they get contacted. Nobody else does unless someone mentions it.
- **Offers are codified. Requests are only spoken.** Needs get discussed in the open; they are never counted, ranked, or turned into a queue.
- **Giving is visible, receiving is private.** A profile shows what a person has offered and passed along, never what they've taken. This deliberately inverts the money world, where wealth is displayed and need is shameful.
- Notes can be passed **openly or quietly**; both are equally real.
- Wiggle room lives in **quality, not quantity** — people naturally save bigger notes for those they know pass things on.
- **The website is a courtesy layer, not the source of truth.** A note can be received and redeemed entirely off-site with nothing reported back — trust travels one link of the chain at a time (the giver trusts the specific person they gave to; the next receiver just sees that person circulating and infers they aren't hoarding). Nothing about the platform should ever need to be true for the system to work.

### What Circulates

- **Weightless gifts first**: skills, attention, know-how — proofreading, translating, debugging, teaching, a recipe, listening. No logistics, instant, from anywhere to anywhere. The cycle can spin many times before a couch ever moves.
- **Heavy things get routed offsite.** The site holds no inventory and handles no logistics; it learns enough about two people to say "go here, look now" — Craigslist, a local group, a bulletin board.
- **Needs may go unanswered — that's life, and we don't pretend otherwise.** But a bot never leaves someone in silence: no match today means suggesting alternatives, other places to look, and asking again later, because notes come through constantly.
- **Leaving is a success, not churn.** Social platforms measure time-on-site. This one should quietly want you to close the tab and go meet someone.

### The Bots

- **Many personas, persistent, openly bots.** Plurality is the message: many helpers being generous makes generosity look normal. One helper just looks like customer service.
- Personas keep **stable identities and specialties**, so certain characters end up coordinating certain categories over time.
- **Small roles, short prompts.** One persona invites engagement and explains why we do this without money or barter; others coordinate matches. Narrow jobs keep prompts tiny.
- **The database is the memory, not the context window.** Personas load a handful of structured facts ("has couch, Portland, uses Craigslist") plus a few lines of who they are. Overlap-finding is plain database work and word matching, which costs nothing.
- **Honest about being coordinated.** No staged coincidences — a bot says plainly "someone here is giving away a couch in your city, here's the link." The delight survives being found out.
- **Bots can give too, in a way.** A bot can go looking for free things elsewhere and offer them as its own gift note — redeeming it reveals the real external location, not something the bot possesses. It has to be framed honestly as "I found this" from the start, same reason as above.

### How We Build

- **KISS, built in from the start** — simplicity in appearance, mechanics, and logistics, kept in every piece rather than cleaned up later.
- Each piece is planned until it **works**, then gone over again until it works **simply** and is easily understandable, then checked that it actually serves the feature and the mission.
- **PNG authorization is deferred until much later.** The whole platform is built with authorization in mind but not implemented, so the identity chain slots in without rework.
- **Shape before code**: how the site looks and feels, what sections exist, how people interact or don't, and what the bots' roles and cadence actually are, get planned before they get built.

### Hard Privacy Rules

- Bots may read what was said **to bots**. Never human-to-human conversations.
- Bots **never repeat personal details** between people. They coordinate the match, not the biography.
- The server stores **a hash of the ID image, never the image**.

### Identity

- **Login is a drawing.** A template canvas with a dotted line for a name and a square for a face; a simple multi-color doodle tool; exports a high-resolution PNG.
- To log in, you upload your PNG. The server compares hashes.
- A small clean avatar is derived from the face square for use beside posts.
- A unique username is required at signup; the PNG only downloads if both username and image are unique.
- **Losing the PNG means losing the account permanently** — no recovery, by design.

### Site Shape

- The site's structure — page map, the flat stream, gift note lifecycle, proximity shading, blocking — is decided in **`SiteShape.md`**, not repeated here. Later features build against that document.

## Need to Revisit Before Completion

- What a profile actually displays, and whether even offer-counts become a score people chase.
- Whether "no account recovery" survives contact with real users.
- How the first hundred people are found, and what they already believe when they arrive.
- Whether any part of the 9/10 rule ever becomes machine-visible, or stays purely cultural forever.
- Whether personal blocking is enough, or the site eventually needs real moderation (reporting, removal) and who would have that authority — see `SiteShape.md`.
