# GitHub Reputation Engine 🛠️

A self-improving "second brain" + operating system for building **genuine GitHub reputation**
through high-quality open-source contributions — run by an AI agent (Hermes Agent or Claude Code),
autonomously, one project at a time.

**Owner:** Basil Al Shukaili ([@basilalshukaili](https://github.com/basilalshukaili))

> Quality of contribution > volume. One merged, appreciated PR beats fifty rejected typo fixes.

## What this repo is

This repo is the **portable brain** of the operation. It lets any agent, on any laptop, continue
the same mission with full context. It contains the plan, live state, reusable playbooks, a
journal of work done, lessons learned, and nightly strategic "dreams."

Start here → [`CLAUDE.md`](./CLAUDE.md) (operating instructions, auto-loaded by Claude Code/Hermes).

## Structure

```
.
├── CLAUDE.md            # Operating instructions — read first (works with Claude Code, Hermes, Codex…)
├── 00-System/           # roadmap, architecture, guardrails (the constitution)
├── 01-Targets/          # the ONE active project + next action
├── 02-Repos/            # per-repo dossiers (stack, conventions, maintainers, opportunities)
├── 03-Journal/          # daily log of what was attempted/done (append-only per day)
├── 04-Playbooks/        # portable, agent-agnostic procedures (triage, PR craft, dreaming)
├── 05-Lessons/          # mistakes & wins → rules for next time
├── 06-Dreams/           # nightly reflective synthesis: patterns, connections, next moves
└── 99-Inbox/            # scratch captures
```

## How it works

```
Brain (top model)  — plans, reviews every diff, writes all maintainer-facing prose, commits
   │ delegates mechanical, fully-specified work
Worker (mid model) — implements to spec, runs tests, triage scans
   │
This repo (state)  — feeds full context back to the Brain on every session
   │
Playbooks (procedure) + Journal/Lessons/Dreams (self-improvement loop)
```

**Token discipline without quality loss:** route cheap/mechanical work to cheaper models; keep
all judgment and human-facing writing on the top model. No output-degrading "compression" tricks.

## Multi-machine usage

- **Laptop A (Hermes Agent):** runs the 24/7 cadence (cron missions + nightly dreaming),
  reports to Telegram. Skills live in Hermes; this repo holds the portable state + playbooks.
- **Laptop B (Claude Code):** clone this repo, open it, and Claude Code auto-reads `CLAUDE.md`.
  The playbooks in `04-Playbooks/` are agent-agnostic, so the workflow is identical.

Pull before you start, commit + push when you finish, so both machines stay in sync.

## Safety

- No secrets are committed (API keys / bot tokens live in each machine's local env).
- Agents fork → branch → PR; never push to an upstream default branch.
- Respects each project's CONTRIBUTING rules and any anti-AI-PR policies.

## License

MIT — see [`LICENSE`](./LICENSE).
