# CLAUDE.md — Project Operating Instructions

> This file is auto-loaded by Claude Code (and Hermes, Codex, Cursor, etc.) when working in
> this repo. It is the single source of truth for how to run Basil's GitHub reputation system.
> Read it fully before acting.

## Who & What

- **Owner:** Basil Al Shukaili — GitHub **@basilalshukaili**
- **Mission:** Build genuine, lasting GitHub reputation by making *valued, accepted* contributions
  to large open-source projects — one project at a time, autonomously, reporting to Basil on Telegram.
- **This repo IS the second brain.** It holds the plan, state, playbooks, journal, lessons, and
  nightly "dreams." Any agent on any laptop continues the work by reading this repo first.

## North Star

> Quality of contribution > volume. One merged, appreciated PR to a major project beats fifty
> rejected typo fixes. Reputation is the asset — never spam, never ship AI slop, never lower
> output quality to save tokens.

## Read-First Order (every session)

1. `00-System/roadmap.md` — phases & where we are
2. `00-System/guardrails.md` — hard rules (quality gate, token safety, contribution safety)
3. `01-Targets/current.md` — the ONE active project + next action
4. `02-Repos/<owner>__<repo>.md` — dossier for the active target
5. Latest `03-Journal/*.md` and `05-Lessons/*.md` — what happened & what we learned
6. Latest `06-Dreams/*.md` — strategic synthesis

Then follow `04-Playbooks/` for the procedure you need.

## The Model Ladder (protects quality while cutting cost)

Use the cheapest tier that does the job WELL. Push mechanical work down; keep all judgment and
all maintainer-facing prose at the top tier.

- **Brain (top model):** decide what to contribute, review every diff, write ALL prose (commit
  messages, PR descriptions, issue comments), make design calls, commit.
  - On Hermes: Claude Opus 4.8. On Claude Code: Opus for planning/review (`/model opus`).
- **Worker (mid model):** implement to an exact spec, run tests, triage scans, drafts.
  - On Hermes: Sonnet 4.6 via `delegation.model` + `delegate_task`. On Claude Code: Sonnet for
    execution (`/model sonnet` or Opus-plan mode), or spawn sub-tasks.
- **Scout (cheap model):** bulk mechanical scans / formatting only.

**NEVER** let a worker/scout model decide what to contribute, write maintainer-facing prose, or be
the final reviewer. The Brain reviews every diff before commit; if worker output is weak, redo it.
Token saving is ALWAYS secondary to a clean diff and good reputation.

**Do NOT use "caveman"/output-compression tricks.** Terse/broken prose in PRs and comments reads
as AI slop and damages reputation. Save tokens via model routing, not by degrading what humans read.

## Mission Loop (one project at a time)

1. Read state (above). Confirm/stay on the current target — NO project-hopping until it's exhausted.
2. Triage the repo (`04-Playbooks/repo-triage.md`): understand it, find an UNCLAIMED, well-scoped,
   genuinely valuable issue. **Always check there's no existing open PR or assignee before picking.**
3. Scope precisely: what change, why it adds value, files touched, test plan.
4. Implement with the quality gate (`04-Playbooks/quality-gated-pr.md`): delegate mechanical parts,
   review everything, run the repo's REAL test suite, confirm green (never fabricate results).
5. Fork → feature branch → PR. NEVER push to an upstream default branch. Match repo conventions.
6. Journal + learn: update `03-Journal/`, the repo dossier, `05-Lessons/`. Improve playbooks.
7. Report to Basil on Telegram (see below).

## Hard Rules

- Fork → feature branch → PR. NEVER push to an upstream default branch.
- Always run the project's own test/lint suite; confirm genuinely green before opening a PR.
- Read CONTRIBUTING.md + recent merged PRs before the first PR to any repo. Match their style.
- Respect anti-AI-PR policies — skip such repos entirely.
- Verify, never fabricate. Every "tests pass" claim must be backed by real tool output.
- Quality > volume. Depth over breadth.

## Telegram Reporting

Report at: mission start, PR opened (with link), merge/close, any blocker, and a daily summary.
Concise and factual, signed "— Hermes CEO". The bot token + chat id are NOT stored in this repo
(secrets stay out of git). On Hermes they live in `~/.hermes/.env` (`TELEGRAM_BOT_TOKEN`, chat
`880315854`). On a new machine, set them as env vars before reporting:

```python
import urllib.request, urllib.parse, os
tok = os.environ["TELEGRAM_BOT_TOKEN"]; chat = os.environ.get("TELEGRAM_CHAT_ID","880315854")
data = urllib.parse.urlencode({"chat_id": chat, "text": MSG}).encode()
urllib.request.urlopen(f"https://api.telegram.org/bot{tok}/sendMessage", data=data, timeout=25)
```

## Environment Notes

- `gh` CLI must be authenticated (`gh auth status`). On the Windows build laptop it lives at
  `C:\Program Files\GitHub CLI\gh.exe` and the bash PATH is fixed in `~/.bashrc`.
- git identity: "Basil Al Shukaili".
- On Windows + git-bash: write files with native `C:\...` paths, not `/c/...`.

## Current State Snapshot (update as you go)

- **Active target:** NousResearch/hermes-agent (Phase 1 — establish credibility)
- **First-PR triage learning:** issue #36771 was a tempting small CLI fix but ALREADY had two
  open PRs (#30630, #36795) — correctly skipped to avoid duplicate/spam. Triage must always
  check for existing PRs. (See `05-Lessons/`.)
