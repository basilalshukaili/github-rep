# System Architecture

## Components

| Layer | Tech | Role |
|-------|------|------|
| Brain | Claude Opus 4.8 (nous provider) | Plans, decides, reviews every diff, writes all prose, commits |
| Hands | DeepSeek (delegation.model) | Mechanical, fully-specified, verifiable subtasks only |
| State | Obsidian vault (Desktop/SecondBrain) | Roadmap, targets, repo dossiers, journal, lessons, dreams |
| Procedure | Hermes Skills + Curator | Reusable playbooks; auto-maintained, self-improving |
| Facts | Hermes memory | Durable user + system facts injected each turn |
| Cadence | Hermes cron | 6h contribution mission + nightly dreaming |
| Channel | Telegram (@Basilclaw_ai_bot) | Reports to Basil (chat 880315854) |
| Tools | gh CLI, git, tmux | GitHub ops, version control, parallel agent spawning |

## The self-improving loop
```
mission run -> journal (03) -> lessons (05) -> nightly dream (06) synthesizes
   -> patches skills/playbooks (04) -> next mission is smarter
   -> memory holds durable facts -> curator prunes/maintains skills
```

## Quality preservation (the core promise)
DeepSeek saves tokens on mechanical work, but NEVER touches output quality because:
- It only executes fully-specified, verifiable tasks.
- Opus reviews every diff and rewrites weak parts.
- Opus writes all judgment-bearing artifacts (commits, PR text, comments, decisions).
- The repo's own test suite must pass (real output) before any PR.

## Token levers (all quality-neutral)
1. Opus plans/reviews; DeepSeek executes mechanical work (~50% Opus reduction).
2. Anthropic prompt caching (never change tools/prompt mid-session).
3. Isolated subagent contexts (delegate_task keeps tool spam out of Opus's window).
4. Scoped reads (read_file/search_files), tool pruning per cron job.
Guardrails prevent ruflo-style runaway: capped iterations, children, timeouts; discrete cron missions.

## Why NOT ruflo/claude-flow
Hermes natively provides what ruflo bolts onto Claude Code (memory, skills, multi-agent
delegation, cron). Ruflo is built for Claude Code, has documented token-explosion issues,
and would add overhead + risk. We use Hermes' native primitives instead — and borrow ruflo's
good ideas (vector memory, pattern store) as concepts in the vault, not as a dependency.

## Operational notes
- gh CLI: `C:\Program Files\GitHub CLI\gh.exe` (not on bash PATH).
- Gateway must run for Telegram routing (`hermes gateway start`; Scheduled Task can be flaky).
- Cron jobs: 2aa772d203dd (contribution, 6h), 1a3ba893c82e (dreaming, 2am).
