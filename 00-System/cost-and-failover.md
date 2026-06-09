# Token & Model Strategy

## Model ladder (cost per 1M tokens)
| Tier   | Model                              | $in / $out | Role                                              |
|--------|------------------------------------|------------|---------------------------------------------------|
| Brain  | claude-opus-4-8                    | 5 / 25     | Decisions, review, all prose, commit messages     |
| Worker | claude-sonnet-4-6                  | 3 / 15     | Mechanical impl, triage, tests                    |
| Scout  | claude-haiku-4-5-20251001          | 1 / 5      | Cheap scans, formatting, grep-style searches      |

Routing pushes cost down ~5x vs all-Opus without quality loss. Sonnet/Haiku handle
mechanical work; Opus keeps all judgment and maintainer-facing writing.

## Token discipline (never at quality's expense)
- Opus plans/reviews; Sonnet executes; Haiku scans.
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