# Feature Summary

- [ ] ID export: render the canvas to a high-resolution PNG the user downloads.

## Description

Add the export step to the Doodle canvas built last task: a "Download my ID" button that renders the drawing to a PNG file the browser saves locally. "High-resolution" here means the canvas's actual pixel buffer is meaningfully larger than its on-screen display size (so the exported PNG isn't a blurry screen-resolution capture) — bump the canvas's internal `width`/`height` attributes up (e.g. to 1200×1200) while keeping its on-screen CSS size smaller (e.g. 480px), which the existing pointer-position math in `draw.html` already handles correctly (it maps screen coordinates to canvas-buffer coordinates via `canvas.width / rect.width`, so drawing at a higher internal resolution than the display size requires no other changes). Export uses the browser's native `canvas.toDataURL('image/png')` plus a plain `<a download>` link — no server round-trip, no new route; the PNG never touches the server until Signup (next feature), which is exactly Mission.md's flow (draw → export → the file itself is what gets uploaded at signup).

- Bump `#idCanvas`'s `width`/`height` attributes to a higher resolution (1200×1200) while its CSS display size stays smaller (`max-width: 480px` already in place) — confirm drawing still lines up correctly on screen (it should, since coordinates are already normalized by the existing `pointerPos()` ratio math).
- Add a "Download my ID" button below the canvas that calls `canvas.toDataURL('image/png')`, sets it as the `href` of a hidden `<a download="my-id.png">`, and clicks it — a standard client-side download, no server involved.
- No new schema, no new route.

## To Do

- Increase the canvas's internal resolution (`width`/`height` attributes) to 1200×1200, keeping the on-screen display size at 480px via existing CSS.
- Add a "Download my ID" button + hidden download link that exports the canvas as a PNG.
- Verify with Playwright: after drawing something, clicking "Download my ID" triggers a download; capture the downloaded file and confirm it's a valid PNG at the higher resolution (1200×1200), not the old 480×480.

## Done

## Details

- No server involvement in this task — the PNG only reaches the server once Signup (next feature) uploads it for hashing.
- Mission.md's "no recovery" property is unaffected by this task; it's just the export mechanism.
