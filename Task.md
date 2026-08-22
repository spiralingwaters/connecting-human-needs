# Feature Summary

User sign-up testing (small fixes) — name decided in hindsight once this task closes

## Description

All 22 features in FeaturesList.md are built and checked off. The user is now downloading the site locally and testing each piece by hand. This task is the catch-all for the small UI/UX fixes that surface during that testing pass — things too small to be their own FeaturesList.md entry. If a fix during testing turns out to be bigger than a small tweak, this task gets closed out (moved to History) and a proper new Task is started for it instead.

- Each small fix found during testing gets fixed directly and logged as a line in Done here, not as its own Task.
- Stays open across the whole review session, picking up fixes as they're found.
- Closes only when the user confirms testing is finished / no more small fixes are coming for now.

## To Do

## Done

- Moved the "That username is taken" signup error to render directly under the username input instead of above the whole form.
- Fixed the drawn ID picture disappearing on a failed signup (taken username, taken drawing, etc.) — the server now hands the submitted username and drawing back, and the canvas restores the drawing instead of resetting blank.
- Added a circle inscribed in the face square on the doodle canvas template (signup.html and draw.html), as a visual hint that the eventual avatar crop could go square or round.

## Details
