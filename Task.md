# Feature Summary

- [ ] Blocking: hide a blocked person's posts, profile, and gift wall from you, and stop their private messages to you — a personal filter, silent, never a platform-wide score or punishment.

## Description

Build the personal filter SiteShape.md describes ("Blocking"): a one-directional table (blocker, blocked) with no platform-visible effect except on the blocker's own view. Blocking someone hides their posts from the blocker's stream view, empties their profile/gift wall *as seen by the blocker*, and stops new messages from them reaching the blocker (existing message history the blocker already has stays visible, per SiteShape.md). Critically: blocking never removes the blocked person's posts from *other people's* views, and other people's posts that `@mention` a blocked user are still visible to the blocker — blocking only removes what the blocked person themself posts/sends, not what others say about or to them. It's silent: the blocked person is never told. No platform score, no moderation action, no admin role — this is purely a per-viewer filter, matching Mission.md's "personal filter... never a platform-wide score or punishment."

- DB: `blocks` table — id, blocker_id, blocked_id, created_at. Unique on (blocker_id, blocked_id).
- `/u/<username>` gets a "Block" / "Unblock" toggle button, visible only when logged in and viewing someone else's profile.
- Blocking effect, applied only to the blocker's own session/view:
  - Stream (`/`, `/search`): posts authored by a blocked user are filtered out of the query for a logged-in viewer who has blocked them. (An `@mention` inside someone else's post text isn't itself a separate row to filter — SiteShape.md already frames this as "you still see other people's posts that @mention a blocked user," which naturally falls out of only filtering by the post's own author.)
  - `/u/<username>` viewed by someone who blocked that user: gift wall and posts sections both render empty (matching "empties their profile and gift wall when you view it") — but the page still resolves and shows the username/Block toggle, it doesn't 404.
  - New messages: `/messages/<thread_id>` POST from a blocked sender should not have been reachable in the first place in the common flow (they'd need to already share a thread), but the read side matters more here — a blocked user's *new* messages shouldn't appear in the blocker's view of the thread going forward; existing history stays. Simplest correct rule matching SiteShape.md: when rendering thread history, hide messages sent by a user the viewer has blocked, dated after the block was created; everything from before the block stays visible.
  - `/messages` list: a thread with a blocked user still appears in the list (existing history is still theirs to keep, per SiteShape.md), it's not deleted — only new incoming content is hidden.
- No block list page is described in SiteShape.md, but a small "Blocked users" list under `/notifications` or similar isn't in scope either — keep this to exactly what's specified: the toggle on the profile page is the only place blocking is managed.

## To Do

- Add `blocks` table to schema.sql (unique blocker_id + blocked_id pair).
- Add `/u/<username>/block` and `/u/<username>/unblock` POST routes (or one toggle route) — logged-in only, can't block yourself.
- Add the Block/Unblock button to `profile.html`, showing current state.
- Filter blocked authors out of the stream query (`index`) and search query for a logged-in viewer.
- Filter a blocked-viewed profile's gift wall + posts to empty, without breaking the page for unknown/other users.
- Filter thread history: hide messages from a blocked sender created after the block's `created_at`; keep everything before.
- Verify with a scripted test-client run: blocking hides the blocked user's stream posts from the blocker only (not from a third party), a blocked user's profile shows empty gift wall/posts to the blocker but normal content to everyone else, a message sent by a blocked user after the block don't show to the blocker but pre-block history still does, unblocking restores everything, blocking yourself is rejected.

## Done

## Details

- Deliberately not a platform-wide filter — every query that respects a block must be scoped to "as viewed by the current logged-in user," never a global exclusion.
- `@mention` filtering explicitly isn't attempted here — SiteShape.md is explicit that other people's posts mentioning a blocked user stay visible; only the blocked user's *own* authored rows get filtered.
