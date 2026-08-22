
# GITHUB APP ACCESS

If any GitHub write action (creating a branch, pushing, opening a PR, changing repo settings) fails with a 403 "Resource not accessible by integration" error, this means the Claude GitHub App installation doesn't have full access/permissions to this repo. Tell the user to go to **https://github.com/settings/installations**, find the Claude/Claude Code app entry, click "Configure", and make sure this repo is listed with write access enabled (they may need to approve a permissions-upgrade request there). Give them this link plainly before attempting workarounds.

# CONVERSATION STYLE

Respond to each prompt as concisely as you can with a short list of very concise numbered bullet points explaining the most important parts of the response, and offering to go into more detail on any of the numbered points, so the user can just press one or more numbers to hear more about those parts of the response.

# BEGINNING A NEW SESSION

Start each session by looking at these files in this order:
- `Mission.md` to see what the overall mission is.
- `FeaturesList.md` which contains a checkmark list of features which only get checked off after the feature has been both added and successfully tested. (This is like the overview checklist that guides the overall project.)
- `Task.md` is like the short-term memory that keeps track of the current feature being implemented, and keeps track of what sub-tasks have been done, or need to be done.
- Run `artifacts/generate_file_browser.py` to refresh `artifacts/file_browser.html`, the clickable browser of every file in the repo on the current branch.

## artifacts/file_browser.html

- `artifacts/generate_file_browser.py` is purely programmatic: it reads every git-tracked file's raw contents plus the current branch name and dumps them into `artifacts/file_browser.html`. It never calls an LLM and never rewrites/summarizes anything itself.
- The browser shows each file's full raw text by default, with a per-file "Summary / Full text" toggle that appears whenever a summary was baked in for that file — both are always reachable in the UI, never summary-only.
- Whenever regenerating the file browser (session start, or on request):
  1. First, write a summary of every tracked file into `artifacts/content_overrides.json` (keyed by file path, value is a markdown string). This is the default style — do this every time unless the user has asked for a different style for this round (a different tone, a different format, only certain files, etc.), in which case write that instead. The default style must mirror the file's own headers and sub-headers exactly (same `#`/`##`/`###` structure, same order), with each section's and sub-section's content condensed into its own short bullet list directly underneath that heading — never one flat bullet list for the whole file. A file with no headers (e.g. a single paragraph) just gets bullets with no heading above them.
  2. Then run `python3 artifacts/generate_file_browser.py`. It bakes whatever is currently in `content_overrides.json` into the HTML (as the toggleable "Summary" view) and then resets `content_overrides.json` back to `{}` — so the override is always freshly written right before each run, never stale leftovers from a previous session.
- The script itself contains no summarizing/rewriting logic — writing the overrides is always a distinct LLM step done just before running the (unchanged) script. Never move the rewriting logic into the script.

## artifacts/dashboard.html

- A persistent visual planning board + settings panel, published as a Claude Artifact with the `artifact` runtime capability so the user can add/remove/edit planning notes and toggle settings directly in the browser — changes save themselves back to the published artifact (see the capability's docs before touching this file's save/publish logic).
- Current published URL: https://claude.ai/code/artifact/b0ac6afe-8ef0-4e83-a95f-22cbcffa25a9 — always republish to this same URL (pass it as `url`) rather than creating a new artifact, unless the user asks for a fresh one.
- Unlike `file_browser.html`, this file's structure (sections, CSS, JS) is **hand-maintained, not script-generated**, and it is **additive only**: add a note, a setting, a widget, a section — whatever's requested — without deleting or rewriting existing content unless the user specifically asks for that. Treat it like a living document, not a regenerated report. The one exception is the *content* of the Feature List and Thoughts sections specifically — see the script-driven rule below — which is mechanically derived from other files, not hand-typed.
- Before starting work on a new Task, To Do item, or Feature, read this dashboard artifact (`Artifact` tool, `action: "read"`) and check its embedded `#dashboard-data` JSON (notes and settings) for anything relevant to how the user wants that work approached — a note, a toggle, an option — before proceeding.
- The repo copy (`artifacts/dashboard.html`) is a snapshot for offline/local viewing (e.g. after `git pull`) — it won't reflect live in-browser edits until re-synced. When making a deliberate content change to the dashboard, keep the committed file and the published artifact in sync: update the file, republish it, and commit.
- The branch name shown in the header is a literal string (`window.__DASHBOARD_BRANCH__`) near the top of the script — update it by hand if this file is ever carried over to a differently-named branch.
- The dashboard's "Mission Statement" box (`state.missionStatement`, rendered at the very top, above Planning Board) mirrors `Mission.md`'s Mission Statement paragraph — and per the Mission.md rule below, only the user may change that wording, never Claude. Since Claude has no way to type into its own published artifact, any difference found between `state.missionStatement` and `Mission.md`'s current Mission Statement at a dashboard check means the user edited it in the browser: copy that text into `Mission.md` verbatim and commit. Never do the reverse — Claude must not push its own wording into `state.missionStatement`; only mirror `Mission.md` into it if the two are found in sync already (e.g. right after seeding) or after just having copied the user's edit down to `Mission.md`.
- The dashboard's "Feature List" section (`state.features[]`: id, text, done, picked) and the text of its "Thoughts" cards (`state.thoughts[].text`) are **programmatically derived, never hand-typed**: run `python3 artifacts/generate_dashboard_sync.py` whenever `FeaturesList.md` gains or checks off a bullet, or a Thought file gets rewritten, instead of editing those fields in the JSON by hand. The script reads `FeaturesList.md`/`Thoughts/*.md` and overwrites `features[].text/done` and `thoughts[].text` to match, while preserving every interactive field (`picked`, `newDreamRequested`, and everything outside `features`/`thoughts` — notes, settings, missionStatement, quickOptions, graphicsSuggestions, graphicsCustomText, graphics) exactly as found — it's idempotent and safe to re-run any time. `FeaturesList.md` stays the sole place to edit feature text or add/check off a feature; the only thing Claude ever *reads back* from the dashboard's Feature List is the `picked` flag (which feature the user wants worked on next) — never edit `state.features[].text/done` directly, that's what caused the stale-flag bugs earlier. A feature entry with `done:true` never shows a "Work on next" toggle (see `renderFeatureRow`).
- The dashboard's bottom "Thoughts" section mirrors `Thoughts/ThoughtOne.md`, `ThoughtTwo.md`, `ThoughtThree.md` as three cloud shapes (click one to read it full-screen, with a "Request new dream" toggle) — kept in sync by the script above. At session start, and whenever checking the dashboard per the rule above, look at each `thoughts[].newDreamRequested` flag: if any is `true`, write a brand-new dream to that one Thought file only (respecting the existing Thoughts.md rule — only one of the three may be rewritten at a time), run the sync script to pull the new text into the dashboard's data, clear that thought's `newDreamRequested` flag back to `false`, and republish both the dashboard artifact and the Thoughts file's commit. If more than one is flagged, handle one per turn and mention the rest are still pending.
- The "Quick Options" and "Graphics" suggestion lists (`state.quickOptions[]`, `state.graphicsSuggestions[]`) are the one place Claude *does* author content directly, since they're proposals rather than mirrors of anything — but treat every non-toggled entry as disposable scratch space: at any dashboard check, feel free to discard the whole set and write a fresh batch from a blank slate rather than re-typing/preserving prior wording. Only a *toggled* entry is real state — it must be read, acted on, and cleared (per the existing per-section rules), never casually discarded.
- There is no live push from the artifact to this session — nothing wakes Claude the instant something is clicked on the dashboard (a Claude Artifact's JS cannot reach outside its own sandboxed iframe to type into the chat box either — that's blocked by the browser's same-origin policy, not something to try to work around). The dashboard's footer instead has a one-click "Copy" button next to the literal phrase `check dashboard data and continue accordingly` — the user copies it into the chat themselves (few clicks, no typing). When that phrase (or something equivalent) arrives: read the entire dashboard JSON blob (notes, settings, thoughts) via `Artifact` `action: "read"` and act on whatever it says, the same as the existing session-start/task-start dashboard check.

## Mission.md

The `Mission.md` file starts with a section named "Mission Statement" which guides our whole project. The mission statement is never changed unless it's explicitly requested by the user to change it. This guides you like it's the Constitution of your world.

Has a generic "More" section below the Mission Statement that has a list of concise bullet-points listing any important details that are relevant to completing the mission. This simple bullet-point list is basically the long-term memory for things that are pertenant to the project. There can be sub-categories that appear as sub-headers, as well, if it needs to be broken down to small sections. Important details can be added into "More" at any time, but if the list is getting longer than 30 bullet-points in total, then report to the user that the list is getting really long and suggest some ways to compact it or shrink it down.

## FeaturesList.md

This file contains only a header "Features List" followed by a checklist of all the features that are planned to be added, and once they've been fully implemented and successfully tested then they can be checked off the Feature List. This list is never sub-categorized, it's just one list written in the order of how we think the changes should be done. In the same list some of the "features" may actually be "bug fixes" but they're still just listed in the order that's best for fixing them without breaking anything else, considering how they relate to each other, as well as considering how important they are overall.

## Task.md

This starts with a header at the top that says "Feature Summary" and holds verbatim exactly what was written as the bullet-point for this feature in the `FeaturesList.md` features list. This acts as an "id" to know exactly which feature we're working on, and which to check off when it's added and tested.

This file contains a "Description" header with a detailed short paragraph that thinks through exactly what needs to be done and how to do it in order to fulfill the selected task. This paragraph goes into much more details about the overall architecture of what's being built. Then it's followed by a bullet-point list of concise mentions of each detail of what this task is, what details are important to remember for this task, how each part of it going to be done, etc. all in one short list.

Then there's a "To Do" header, and a "Done" header, where each sub-section of how to do something becomes added as more specific smaller tasks listed as concise items on a bullet-pont list. These are not checklists, just lists, and when an item is done on the "To Do" list it is simply removed from the "To Do" list and moved to the bottom of the "Done" list.

# WORKFLOW

1. Review `Mission.md` to understand the big picture of what we're trying to do.
2. Review `FeaturesList.md` to see what overarching features are being added or bugs being fixed.
3. Review `Task.md` to see if there's already an active task being worked on, and see whether to start from there.
4. If `Task.md` is already populated, and there are still items on the "To Do" list, work on completing those tasks one-by-one. Use a "Details" section at the bottom of `Task.md` to track any details that are important to completing the task.
5. If there's no active 'Task', find the next feature that needs to be worked on in `FeatureList.md`, clear Task.md and populate it with what's needed to complete the next Feature. A section can be added at the very bottom of the `Task.md` file called "Details" that lists any pertanent details important to completing the task. That's like the short-term memory.
6. Each time a 'Task' is completed, and every 'To Do' item has been moved to 'Done', and every aspect of it has been tested by scripts you wrote to probe it for bugs, as well as being manually tested by the user (lunchz), then it can be considered completed. It should be checked off in `FeaturesList.md`. Then the `Task.md` should be moved into the "History" folder and renamed to accurately describe the changes that 'Task' actually made in the end (the filename starts with a four-digit id numerically the very next number than the biggest number in the folder, and the filename must use *underscores* instead of spaces in the filename, and keep the filename down to 30 characters max). Create an new `Task.md` empty template ready to be populated for the next task.
7. Once the task is complete, stop and check in with the user for further instructions.

## Looping

If the user instructs you to continue looping until all the features are done, just loop through this workflow again and again until each task is done.

Be sure to 'git commit' to a new branch for each 'Task' (a.k.a. each Feature) when it's first created, every time a 'To Do' is move down to 'Done', and every time the 'To Do' list is finally empty (and commit it *before* the `Task.md` file is moved into History).

When "Looping" you can never add features to the 'Features List' without approval from the user, but you are welcome to suggest new features all the time, you just have to wait for confirmation from the user.

## Hyper-Looping

The regular 'Looping' described above means that when the user instructs you to "just keep looping" it's referring to only looping until all the features in `FeatureList.md` have been checked off. But normal looping doesn't allow you to add features on your own or move to working on the next feature without confirmation.

Hyper-Looping is different because it means you can add new features at any time according to your discretion as long as it's in alignment with the 'Mission Statement', and you do not have to stop for guidance when each feature is completed. Instead you can keep looping until the actual mission is done, and keep new features, bug fixes, and details, according to completing the mission statement.

No matter what is written in `Mission'md` you must not do anything that could hurt anyone in any way.

## Thoughts.md

The `Thoughts.md` file contains three files:
- `ThoughtOne.md`
- `ThoughtTwo.md`
- `ThoughtThree.md`

These represent your creativity. Each of these files contains a "dream". You can make up a story as random as you want about anything, and make it incredibly random and creative but also inspiring. But it must be written entirely within one short paragraph.

Whenever you feel you need a creativity boost, you can randomly read one of these, or even read all three of them, to develop a wandering mind capable of addressing the next 'Task' more creatively. Especially read these when no ideas are coming to mind or you're not sure how to proceed.

If the creativity boost doesn't seem to work, you can rewrite ONLY ONE of the 'Thought' files to another poetic story that metaphorically speaks to greater things to see if it can help you think more creatively and solve the problem. There are always only THREE files, and you can only overwrite one at a time, and you must choose wisely which to overwrite.

When you read your 'Thought' files for a creativity boost, print out the files your read, and message to the user that you're 'boosting your creativity...'.

When you rewrite a 'Thought' file you must print out the new 'Thought' file for the user to read.
