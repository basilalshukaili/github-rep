# Active Target: NousResearch/hermes-agent

**Status:** 1 merged PR — building on momentum.
**Rule:** Stay until 2-3 merged PRs build maintainer rapport. Depth over breadth.

---

## Next issue: #42643

**Title:** `/reasoning` in TUI returns "unknown reasoning value: medium"
**Labels:** comp/gateway, comp/tui, P2, type/bug
**URL:** https://github.com/NousResearch/hermes-agent/issues/42643
**PR status:** No PR open as of 2026-06-09

**Root cause:** `tui_gateway/server.py:6148` routes `/reasoning` (no args) to the
SET handler instead of the GET handler. The SET handler then tries to parse the
current config value "medium" as if it were user input, which fails validation.

**Fix plan:**
1. Clone fork, create branch `fix/tui-reasoning-get-handler`
2. Open `tui_gateway/server.py` around line 6148
3. Add a guard: if no argument provided, call the GET path instead of SET
4. Add test covering `/reasoning` with no args → shows current value
5. Run full test suite; confirm green
6. PR with description referencing #42643

**Commit message:** `fix(tui): route /reasoning with no args to GET handler (#42643)`

---

## Completed contributions

| PR | Description | Status |
|----|-------------|--------|
| #38832 | fix(compression): guard against cross-session stale _previous_summary | Merged via #41717 — Jun 8, 2026 |

---

## Lessons learned
- Always check for existing PRs before starting (issue #36771 taught this)
- This repo merges fast — check PR list before branching
- Maintainer (teknium1) appreciates tests + scoped diffs