# Feature Summary

- [ ] Doodle canvas: template with a dotted name line and a face square, a few colors, an eraser, and a clear button.

## Description

Build the drawing surface Mission.md describes as the real login's core: "a template canvas with a dotted line for a name and a square for a face; a simple multi-color doodle tool." This task is purely the drawing UI — no export, no hashing, no signup wiring yet (those are the next three features). A plain HTML5 `<canvas>`, drawn with mouse/touch, with a faint permanent template layer (a dotted line near the bottom for the person to write their name over, and an outlined square for a face doodle) that stays visible under the drawing but isn't itself part of what gets exported as "drawn" content later — it's just a guide. A few color swatches to pick a pen color, an eraser toggle, and a clear button that wipes the user's drawing back to blank (template guide reappears). Keep this dead simple: no undo stack, no brush size slider, no layers — KISS.

- New route `/id/draw` (no login required — this happens *before* an account exists, per Mission.md's identity flow) rendering a canvas page.
- Template guide: a dotted line roughly a third of the way up from the bottom (for the name) and an outlined square above it (for the face), drawn in a light, unobtrusive color directly onto the canvas as a non-erasable background layer (redrawn under the user's strokes any time the canvas is cleared or on load).
- A small palette: 4-6 fixed colors (e.g. black, red, blue, green, plus maybe orange/purple) as clickable swatches, one active at a time.
- An eraser toggle: switches the pen to erase (clear to background) instead of draw.
- A clear button: wipes all user strokes, redraws just the template guide.
- Pure client-side JS + canvas — no new DB table, no server-side drawing state; this page doesn't submit anything to the server yet (that's ID export next).
- Works with both mouse and touch input (pointer events), since a phone is a very plausible way to draw this.

## To Do

## Done

- Added `/id/draw` route + `draw.html` template with a `<canvas>` element.
- Drew the template guide (dotted name line + face square outline) as a background layer, redrawn on load and after clear.
- Wired up freehand drawing via pointer events, respecting the active color.
- Added color swatch buttons that set the active pen color.
- Added an eraser toggle button that switches strokes to erase mode.
- Added a clear button that wipes user strokes and redraws the template guide.
- Verified in a real browser via Playwright: drew a stroke, switched to red and confirmed the canvas changed, toggled the eraser and confirmed its active state, clicked clear and confirmed the canvas reset — also visually confirmed with a screenshot (face square, dotted name line, and drawn strokes all render correctly).

## Details

- No export/download yet — that's ID export, next feature. This task's canvas doesn't need to produce a file.
- No login gate on this route — Mission.md's flow is draw first, then sign up with the drawing, so an account can't exist yet when this page is used.
