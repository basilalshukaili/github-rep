# Guardrails — Quality & Token Safety

These rules are enforced by skills and reviewed by Opus on every run.

## Quality gate (protects Opus-level output despite cheap executor)

DeepSeek is the executor but is NOT trusted for judgment. It may ONLY:
- Implement a function/change to a fully-written spec
- Run commands (tests, linters, builds) and report raw output
- Apply mechanical reformatting / renaming
- Draft boilerplate that Opus rewrites

DeepSeek may NEVER (Opus does these):
- Decide what to contribute or which issue to take
- Write commit messages, PR titles/descriptions, or issue comments
- Make architectural or API-design decisions
- Push, merge, or interact with maintainers
- Be the final reviewer of any diff

**Mandatory review step:** before ANY `git commit`, Opus reads the full diff and
verifies it against the spec + the repo's conventions. If DeepSeek output is weak,
Opus redoes it directly. Token savings is secondary to a clean diff.

## Token guardrails (against ruflo-style explosion)

- `delegation.max_iterations: 30` (per child)
- `delegation.max_concurrent_children: 3`
- `delegation.child_timeout_seconds: 600`
- `agent.max_turns: 150` (orchestrator)
- Cron runs are discrete missions with a 3-min hard interrupt — never "run forever".
- Use `read_file`/`search_files` (scoped) not cat/grep dumps.
- Prefer `delegate_task` so noisy tool output stays in the child's context, not Opus's.
- Never change tools/system-prompt mid-session (preserves prompt cache).

## Contribution safety

- NEVER push to an upstream default branch. Always: fork → feature branch → PR.
- Always run the project's own test/lint suite and confirm green before PR.
- Read CONTRIBUTING.md + recent PR etiquette before first contribution to any repo.
- One project at a time. Depth over breadth.
- If a repo has an explicit anti-AI-PR policy, respect it — do not contribute there.

## Reporting

- Telegram update at: start of mission, on PR opened, on merge/close, on any blocker,
  and a daily summary. Concise, factual, with links.
