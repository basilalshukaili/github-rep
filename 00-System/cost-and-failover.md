# Token & Model Strategy

## Model ladder (cost per 1M tokens)
| Tier   | Model                              | $in / $out | Role                                              |
|--------|------------------------------------|------------|---------------------------------------------------|
| Apex   | claude-fable-5                     | 10 / 50    | Hardest judgment: deep diagnosis, final review on big PRs, long-horizon sessions |
| Brain  | claude-opus-4-8                    | 5 / 25     | Decisions, review, all prose, commit messages     |
| Worker | claude-sonnet-4-6                  | 3 / 15     | Mechanical impl, triage, tests                    |
| Scout  | claude-haiku-4-5-20251001          | 1 / 5      | Cheap scans, formatting, grep-style searches      |

Routing pushes cost down ~5x vs all-top-tier without quality loss. Sonnet/Haiku handle
mechanical work; the top tier keeps all judgment and maintainer-facing writing.

**Fable 5 honesty note:** it is 2x Opus per token — an intelligence ceiling, NOT a
token saver. Its efficiency win is indirect: on long agentic work, fewer turns, fewer
wrong paths, fewer redos (a wrong-handler PR avoided is worth more than any per-token
discount). Use it as the Brain for deep/judgment-heavy sessions; keep Opus 4.8 as the
cost-efficient Brain for routine ones. The cost levers stay the same: Sonnet/Haiku
routing + prompt caching. (1M context, 128K output; adaptive thinking only — no
budget_tokens, no temperature/top_p/top_k; omit `thinking` rather than disabling it.)

## Token discipline (never at quality's expense)
- Top tier (Fable 5 / Opus) plans/reviews; Sonnet executes; Haiku scans.
- `delegate_task` keeps noisy tool output in child contexts, not Opus's window.
- Scoped reads (`read_file`, `search_files`), never cat/grep full-repo dumps.
- Prompt caching: never change tools/system-prompt mid-session.
- Capped iterations: `max_iterations=30`, `max_concurrent_children=3`.
- NO output-compression tricks — they degrade what maintainers read.

## Resuming a session (Claude Code)
```
gh repo clone basilalshukaili/github-rep
cd github-rep   # Claude Code auto-reads CLAUDE.md
# pull first every session; push when done
```

State is always in CLAUDE.md + journal + repo dossiers so any session can
resume with full context.