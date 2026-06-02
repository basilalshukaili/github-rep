# Cost & Failover Strategy

## The constraint
- Nous credits are limited (~$7 at last check). A 24/7 Opus cadence WILL eventually exhaust them.
- Basil will NOT top up here — work continues on the OTHER laptop via Claude Code.
- Therefore: when credits run low/out, the #1 priority is **lose no progress** — everything must
  be committed and pushed to the second-brain repo so Claude Code can resume seamlessly.

## Model ladder (cost per 1M tokens, all on nous)
| Tier   | Model                      | $in / $out | Role |
|--------|----------------------------|-----------|------|
| Brain  | anthropic/claude-opus-4.8  | 5 / 25    | Decisions, review, all prose, commits |
| Worker | anthropic/claude-sonnet-4.6| 3 / 15    | Mechanical impl, triage, tests (delegation.model) |
| Scout  | anthropic/claude-haiku-4.5 | 1 / 5     | Cheap scans/formatting |

Routing mechanically pushes cost down ~5x vs all-Opus, WITHOUT quality loss (Sonnet/Haiku do
mechanical work; Opus keeps all judgment + maintainer-facing writing).

## DeepSeek = "save progress" failover ONLY (not a creative worker)
**Why not auto-fallback to DeepSeek for contribution work?** Because if Opus is exhausted mid-task,
a DeepSeek continuation would produce lower-quality contribution work — exactly what we must never
ship. Basil explicitly said: *DeepSeek's job is only to push what we already reached, save progress,
NOT create new things.*

**Design: a dedicated lightweight commit-and-push watchdog cron, run on DeepSeek.**
- It does NOT triage, code, or open PRs. It ONLY ensures the second-brain repo (and any local
  work-in-progress in cloned contribution repos under our control) is committed and pushed so
  nothing is lost.
- It runs cheaply and frequently as a safety net. If there's nothing to save, it stays silent.
- Cron job: "Save Progress (DeepSeek failover)" — see `hermes cron list`.

DeepSeek credentials: `DEEPSEEK_API_KEY` in `~/.hermes/.env`. Endpoint https://api.deepseek.com,
model `deepseek-chat`. (Key should be ROTATED — it was pasted in chat once.)

## What happens when Opus credits run out
1. Contribution missions (Opus) will start failing / erroring on the model call.
2. The DeepSeek "Save Progress" job keeps committing + pushing state regardless — no work is lost.
3. Basil pulls the repo on the other laptop and continues with Claude Code, fully in context
   (CLAUDE.md + journal + dreams tell Claude Code exactly where things stand).

## Resuming on the other laptop (Claude Code)
```
gh repo clone basilalshukaili/github-reputation-engine
cd github-reputation-engine   # Claude Code auto-reads CLAUDE.md
# git pull first every session; git push when done
```

## Token discipline (recap — never at quality's expense)
- Opus plans/reviews; Sonnet executes; Haiku scans.
- delegate_task keeps noisy tool output in child contexts, not Opus's window.
- Scoped reads; prompt caching; capped iterations (max_iterations=30, max_concurrent_children=3).
- NO output-compression/"caveman" tricks — they degrade what maintainers read.
