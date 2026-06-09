# Lesson: reproduce the bug and locate the REAL handler before fixing

**Date:** 2026-06-09 — source: hermes-agent #42643

## What happened
A worker produced a clean, fully-tested fix for the `/reasoning` TUI bug — but it patched
`config.set`, while bare `/reasoning` is routed to `config.get`. The fix sat on a dead code
path and would not have fixed the reported error. The bug also did not reproduce on current
`main` (the relevant guards landed in April). Opening that PR would have drawn a
"wrong handler / cannot reproduce" from a sharp maintainer and damaged reputation — the exact
opposite of the mission.

## The rule (apply before any external-repo fix)
1. **Reproduce on current `main` first.** If it does not reproduce, the issue may be stale or
   environment-specific — say so and ask the reporter; do NOT ship a speculative fix.
2. **Grep the exact error string** to find the handler that actually emits it.
3. **Trace the real call path** (which client/route reaches that handler) before editing.
4. **Check git history/dates** of nearby guards — the fix may already have landed.
5. The Brain (Opus) reviews every worker diff against the real code before any PR. A plausible,
   tested, WRONG fix is worse than no PR. Token-saving never overrides this.

## Attribution corollary
Every contribution commit MUST be authored `Basil Al Shukaili <basilalshukaili@gmail.com>`.
A stray `lordbasil147@gmail.com` merge commit got attributed to the `dhofaroffice365` account
and blocked the haystack #11492 CLA. Set `git config user.email basilalshukaili@gmail.com` in
every clone; if a stray identity slips into a PR, re-author (`git commit --amend --reset-author`
or rebase `--exec`) and force-push the fork — the CLA re-checks and clears.
