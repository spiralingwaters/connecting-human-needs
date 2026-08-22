# Feature Summary

- [ ] Search: find stream posts by keyword. Tentative ranking plan (tiered by term match, newest-first within each tier) in SiteShape.md "Open for later tasks" — still not finalized.

## Description

Build keyword search over the stream using the tentative ranking plan already written down in SiteShape.md: split the query into terms, group results into three tiers — all terms match, then some terms match, then only one term matches — newest-first within each tier. This is explicitly tentative (not finalized), so keep the implementation simple and easy to re-tune rather than over-building it: plain SQL LIKE matching against `posts.body` (and `author_name`, since `@username` mentions are inline text per SiteShape.md), no full-text index, no external search engine. `/search?q=...` renders using the same post markup as the stream, with each tier visually separated per SiteShape.md ("a colored band/strip framing that tier, not the post box itself") — proximity/redeemed shading isn't implemented yet (Public feed deferred it), so for now this only needs the tier-band styling, not real distance shading. A search box goes in the header or near the top of `/`, submitting GET to `/search`.

- `/search?q=<query>` — splits `q` on whitespace into terms, runs three queries (or one query with tier computed in Python) to bucket posts by how many distinct terms matched, orders each bucket by id desc, renders three optional sections.
- Reuses the existing `.post` / `.stream` markup for individual posts; adds a wrapping section per tier with a label and a distinct background band.
- Empty query or no matches: simple "no results" messaging, no crash.
- Search box: a simple GET form, no autocomplete/live search — KISS.
- Out of scope: proximity shading integration (doesn't exist yet), search ranking finalization (still tentative per SiteShape.md — revisit if that doc's plan changes).

## To Do

- Add `/search` route: parse `q` into terms, bucket matching posts into 3 tiers, newest-first within each.
- Add `search_results.html` template (or extend index.html) with tier sections and bands.
- Add a search box (GET form) to the header/stream area, wired to `/search`.
- Style the tier bands per SiteShape.md wording (background/strip behind each tier section, not the post box itself).
- Verify with a scripted test-client run: query matching all terms in one post ranks in the top tier, a post matching only one of two terms lands in the bottom tier, empty query and no-match query both render without error, search box on `/` reaches `/search`.

## Done

## Details

- Ranking plan is explicitly "tentative — not yet built or visually finalized" per SiteShape.md; if the user later firms up the plan differently, this implementation is expected to be revisited, not a bug.
- No proximity shading yet, so tier bands are the only visual grouping for now — don't invent shading logic that doesn't exist elsewhere in the app yet.
