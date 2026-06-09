# NousResearch/hermes-agent — Contribution Dossier

**Repo:** https://github.com/NousResearch/hermes-agent
**Stars:** ~175k | **License:** MIT | **Language:** Python 3.11
**Status:** ACTIVE — first merged PR landed June 8, 2026

---

## Merged contributions

### PR #38832 — fix(compression): guard against cross-session stale _previous_summary contamination
- **Opened:** June 2026 | **Closed/Merged:** June 8, 2026 via PR #41717
- **Problem:** Cron/background sessions left stale `_previous_summary` on the shared
  `ContextCompressor` instance. Subsequent live sessions picked it up and injected
  unrelated prior context into the summarizer prompt, poisoning live conversations.
- **Fix:** Added guard in `compress()` (line 1911): if no handoff summary exists in
  current messages but `_previous_summary` is non-empty, discard it and start fresh.
- **Tests:** 3 new test cases in `tests/agent/test_context_compressor_cross_session_guard.py`
  (stale clear, handoff preservation, non-interference). All 33 tests green.
- **Credit:** teknium1 merged the approach in PR #41717 with Basil listed as co-author
  and added to `AUTHOR_MAP` in `scripts/release.py`.
- **Fixes issue:** #38788

---

## Development notes

- Windows testing requires `PYTHONPATH=$(pwd)` and `pytest -n 0`
- Commit convention: `type(scope): subject` (fix, feat, chore, docs, test)
- New tools must include a `check_fn`
- Check existing PRs before opening — this repo moves fast, duplicates happen

## Next contribution candidates

Triage in progress. Prioritize unclaimed P2/P3 bugs in:
- `agent/` — delegation edge cases
- `cron/` — scheduling reliability
- `hermes_cli/` — Windows/CLI quirks
- Documentation gaps where deep knowledge adds real value

Rule: check for existing PRs on any issue before starting work.