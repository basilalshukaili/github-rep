# Dossier: NousResearch/hermes-agent

## Identity
- Repo: NousResearch/hermes-agent — https://github.com/NousResearch/hermes-agent
- Stars: ~175k · very active
- License: MIT
- Primary language: Python
- AI-PR policy: none found prohibiting it (verify CONTRIBUTING before first PR).

## Why this is target #1
- We run this framework daily — deep, hard-to-replicate familiarity.
- Strong niche: first-hand Windows quirks, skills/curator, delegation, cron.
- Dogfooding: every fix improves Basil's own tooling.

## Stack & Tooling
- Language: Python (3.11)
- Tests: pytest (`python -m pytest tests/ -o 'addopts=' -q`). On Windows, install pytest +
  pytest-xdist + pyyaml into a system Python 3.11 and run with `PYTHONPATH=$(pwd)` and `-n 0`.
- Layout: run_agent.py, agent/, hermes_cli/, tools/, gateway/, cron/, tests/, website/.

## Conventions
- Commit style: `type: subject` (fix:, feat:, refactor:, docs:, chore:).
- New tools need a `check_fn`. Use `get_hermes_home()` for paths. Never break prompt caching.

## Opportunities (triage in progress)
| Issue | Link | Value | Tractability | PR exists? | Notes |
|-------|------|-------|--------------|-----------|-------|
| #36771 claw migrate wrong cmd | issues/36771 | low | trivial | **YES (#30630, #36795)** | SKIP — duplicate |
| (more candidates being triaged) | | | | | |

## First contribution
- Not yet chosen. #36771 rejected (already has 2 open PRs). Triaging unclaimed P2/P3 bugs next,
  weighting toward our Windows / CLI / delegation / cron knowledge.

## Contribution log
- (none yet)

## Lessons specific to this repo
- Small obvious bugs here get PR'd fast — check existing PRs first. See
  [[05-Lessons/always-check-for-existing-pr]].
