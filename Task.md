# Feature Summary

- [ ] Offsite routing: help a giver post somewhere real and point the receiver at it.

## Description

Per Mission.md ("Heavy things get routed offsite. The site holds no inventory and handles no logistics; it learns enough about two people to say 'go here, look now'"), this is assistance, not automation: the site cannot actually post to Craigslist or any third-party service on a user's behalf (no API integration is in scope, and fabricating one would misrepresent what the site does). What it *can* honestly do: help the giver produce good copy-paste-ready listing text from a gift note they've already written, and give the holder a real, working link to go look somewhere external. No geolocation exists yet (deferred since Public feed), so the "somewhere real" link is a generic external search — not a city-specific one — clearly labeled as such rather than pretending to be localized.

- On the held-note view (`/notes`), for each held note, add a "Get posting text" action: renders (no new route needed for viewing — a simple inline `<details>`/expand block populated server-side is enough) a copy-paste-ready listing built from the note's title/description/contact — this is for the *original author* to use if they want to also list the item somewhere with real reach (a local Craigslist/Facebook Marketplace/Freecycle post), not something the site submits anywhere itself.
- On the same held-note view, add a "Look elsewhere too" link per note: a real, working URL to Craigslist's free-stuff search for the note's title (e.g. `https://www.craigslist.org/search/zip?query=<title>&sort=date` scoped to the "free" category via their search params) — since there's no user location yet, this omits a specific city (Craigslist's own site handles the "pick your region" step) rather than guessing one.
- This is entirely presentational — no new DB table, no new route beyond what's needed to render the two pieces on the existing `/notes` page.
- Being explicit about what this is *not*: not an integration, not an auto-post, not proof anything was actually listed anywhere. The copy-paste text is a convenience; the link is a real starting point, nothing more.

## To Do

- Build the copy-paste listing text (title + description + contact, formatted as plain text) directly in `notes.html`'s Jinja template for the holder's own view — no server-side change needed since it's simple string composition of fields already passed to the template. (If composition needs to be non-trivial, do it in the `notes()` view instead of the template.)
- Add a real Craigslist free-search link per note using the note's title as the query, with a plain-text caveat that it's not a personalized/city-specific search since location isn't available yet.
- Verify with a scripted test-client run: `/notes` renders both the listing text block and the search link for each held note without erroring, and the link URL is well-formed (contains the note's title, URL-encoded).

## Done

## Details

- No external API call, no scraping, no claim of automation — this is copy/paste assistance plus a real link, matching what the site can honestly do without an integration decision (which, like the LLM question, is an infrastructure/API choice left for later, not guessed at here).
- Revisit once geolocation exists (Public feed's deferred proximity data) to make the external link city-specific.
