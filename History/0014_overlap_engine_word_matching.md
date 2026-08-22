# Feature Summary

- [ ] Overlap engine: plain database matching to find who has what someone else needs, and whether they're reachable to each other.

## Description

Build the plain-SQL matching Mission.md describes explicitly as non-LLM work ("Overlap-finding is plain database work and word matching, which costs nothing"). Using the `user_facts` table Fact extraction populates, find pairs where one person's `needs` fact text overlaps (word-level) with another person's `offers` fact text — a simple word-overlap score, no embeddings, no external service. "Whether they're reachable to each other" just means: both users have to actually exist and not have blocked one another (reuse the `blocks` table from Blocking) — there's no location/proximity data yet (deferred since Public feed), so reachability here is purely "not blocked," not a distance check.

- A pure function/query, no new schema needed: `find_overlaps(db, user_id)` — for a given user's `needs` facts, scan every other user's `offers` facts, score by shared significant words (lowercased, simple stopword-free word-set intersection), return matches above a small threshold (at least one shared word), best-scoring first, excluding any pair where either has blocked the other.
- This task builds the engine and a way to see it work (a small `/overlaps` page for a logged-in user showing their current candidate matches, read-only) — it does **not** send anything to anyone. Reaching out is explicitly Coordinator bots' job next; this task only finds and displays candidates.
- Keep the scoring dead simple and explainable: split both fact values into lowercase word sets (dropping a short stopword list: a, an, the, to, for, and, of, in, i, need, needs, looking, have, offer, offering — the verb/filler words the extraction patterns themselves tend to capture), count shared words, require at least 1.

## To Do

## Done

- Added `find_overlaps(db, user_id)` to app.py: joins the user's `needs` facts against other users' `offers` facts, scores by shared significant-word count, filters out blocked pairs (either direction), orders best-first.
- Added `/overlaps` route (logged-in only) + template: lists candidate matches (other user's username, their matching offer text, the searching need text).
- Verified with a scripted test-client run: a shared-word need/offer pair matches, an unrelated need finds nothing, blocking either party removes the match.

## Details

- Deliberately plain word-overlap, not any embedding/semantic similarity — matches Mission.md's explicit "costs nothing" framing for this piece.
- Location/proximity weighting from SiteShape.md ("Weighs candidates near the original giver") isn't available yet (no geolocation data exists) — this task only builds the word-overlap half; proximity weighting is a follow-up once location data exists, flagged rather than silently skipped.
