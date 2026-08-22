# Feature Summary

Tethered post & search bar: a minimal search bar fixed to the top of the page and a compose box fixed to the bottom, both always visible while scrolling — replacing the current inline search form and the separate "New post" page with chrome that stays put like a social-media app.

## Description

Right now `index.html` puts a full search form and a "New post" link inline at the top of the page, above the stream, and posting happens on a separate `/new` page. This task turns both into persistent chrome: a slim search bar fixed to the top of the viewport (`position: sticky` or `fixed`, minimal height, always reachable while scrolling the stream) and a compose box fixed to the bottom of the viewport for logged-in users, so posting is a one-field-and-a-button action available from anywhere on the page without navigating away. Both bars stay out of the way of the content — the stream scrolls underneath/between them, with body padding added so posts are never hidden behind the fixed bars. The bottom compose bar posts via a small inline form (same `/new` POST endpoint, reused for both the fixed bar and — decision pending below — the old page) and, given the user's earlier answer, is hidden entirely (not shown as a login prompt) for logged-out visitors, since reading is public but posting requires an account. The top search bar keeps using the existing `/search` GET endpoint and result page; only its position/size changes, not its behavior. Styling should feel closer to a modern social app: compact, rounded, unobtrusive, using the site's existing accent color and fonts rather than introducing a new visual language.

- Top bar: fixed/sticky to top of viewport, minimal height, contains just the search input + submit (icon or short button), reuses `/search` GET behavior — no functional changes to search itself.
- Bottom bar: fixed to bottom of viewport, minimal height, contains just a text input (or small textarea) + submit, posts to `/new` (reuse existing POST logic), only rendered when `current_user` is set — logged-out visitors see no bottom bar and no reserved space for it.
- `main` content needs top/bottom padding equal to the bars' heights so posts at the start/end of the stream aren't hidden underneath the fixed chrome.
- Decide whether the standalone `/new` page (`new_post.html`) is removed, kept as a fallback/redirect to `/`, or left as-is for non-JS/direct-link access — leaning toward keeping the route but having it just redirect to `/` since the bottom bar now covers composing on every page that extends `base.html`.
- Should work with plain HTML forms (no JS required) so it degrades gracefully; a touch of JS is fine for polish (e.g. clearing the input after submit) but not required for correctness.
- Test manually: search still works and returns results, posting from the bottom bar appends to the stream without a page reload feeling broken, logged-out view has no bottom bar, fixed bars don't overlap/hide content at top or bottom of a long stream, responsive on a narrow viewport.

## To Do

- Update `build/static/style.css`: add fixed/sticky positioning + compact styling for the new top search bar and bottom compose bar; add `main` padding to clear both.
- Update `build/templates/base.html` and/or `index.html`: move the search form into a fixed top bar (present on every page, or just index? — leaning toward every page via `base.html` so search is always reachable, matching "search bar... always tethered to the top of the screen"), and add the fixed bottom compose form to `base.html`, gated on `current_user`.
- Remove the old inline `.search-form` and `.compose-link` markup from `index.html` once superseded by the fixed bars.
- Decide and implement the fate of the standalone `/new` GET page (redirect to `/` vs. keep as fallback).
- Manually test: logged-in posting from the bottom bar, logged-out view (no bottom bar), search from the top bar, scrolling a long stream to confirm no content is hidden under either bar, narrow-viewport layout.
- Update `FeaturesList.md` (check off) and move `Task.md` to `History/0024_...md` once done and confirmed by the user.

## Done

## Details

- Decision from user: logged-out visitors see no bottom compose bar at all (not a "log in to post" prompt) — no reserved space, full-width stream.
- Reuse existing `/search` and `/new` POST endpoints as-is; this task is presentation/layout only, not new backend behavior.
- Site-wide fixed bars (via `base.html`) vs. index-only is still open — will default to site-wide for the top search bar (matches "search bar should probably always be tethered to the top of the screen") and bottom compose bar only where `current_user` is set, unless the user says otherwise.
