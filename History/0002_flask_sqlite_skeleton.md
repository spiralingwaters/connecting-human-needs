# Feature Summary

- [ ] Project skeleton: server, database, and a single styled page that renders.

## Description

Stand up the minimal `build/` tree that the rest of the site grows from: a small server, a database, and one styled page that actually renders in a browser — nothing else yet (no auth, no feed, no bots). Keep it KISS: no compile step, no bundler, server-rendered HTML only, so `build/` stays the literal source tree. Pick the lightest stack that runs happily behind nginx (per dashboard note: "must work on nginx") — a Python (Flask) app served via a WSGI process, reverse-proxied by nginx, with SQLite as the database (file-based, zero setup, fine for this stage). The one page rendered is the `/` route from SiteShape.md (Global stream placeholder) with basic shared styling, proving the server-render + DB read/write path works end to end before any real feature logic lands on top.

- Server: Flask app in `build/`, single process, reads/writes SQLite.
- Database: SQLite file + a minimal schema/migration approach (plain `.sql` files, no ORM migration framework — KISS).
- Page: `/` route renders server-side HTML from a template, pulls at least one value from the DB to prove the read path, uses a shared base stylesheet (plain CSS, no build step).
- Nginx: document how the app is meant to be reverse-proxied (README note or comment), not a full deploy script — just needs to be nginx-compatible (bind a local port, no assumptions that break behind a proxy).
- No auth, no posting, no bots yet — those are later features.

## To Do

## Done

- Decided file layout inside `build/` (app.py, templates/, static/, db/).
- Added SQLite schema file + seed data.
- Added Flask app with `/` route rendering a template.
- Added base stylesheet and confirmed the page renders styled (verified via test client — tagline pulled from DB, CSS linked).
- Documented nginx reverse-proxy requirements in `build/README.md`.
- Wrote `build/README.md` covering how to run it.

## Details

- Must work behind nginx (dashboard note from user).
- KISS per Mission.md "How We Build" — simplicity built in from the start, not cleaned up later.
- This skeleton intentionally does nothing else — placeholder identity, feed, gift notes etc. are separate later features in FeaturesList.md.
