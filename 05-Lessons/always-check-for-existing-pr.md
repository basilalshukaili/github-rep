# Lesson: Always check for an existing PR before picking an issue

**Date:** 2026-06-01
**Context:** First triage of NousResearch/hermes-agent. Found issue #36771 — a clean, well-documented
small CLI bug (`hermes claw migrate` suggested `hermes stop` instead of `hermes gateway stop`),
with the exact one-line fix specified by the reporter. Looked like a perfect first PR.

**What happened:** Before implementing, triage checked open PRs referencing the issue:
`gh pr list --repo NousResearch/hermes-agent --state open --search "36771"`. Found it was ALREADY
addressed by TWO open PRs (#30630 and #36795). A maintainer/commenter had also noted the duplicate.

**Rule for next time:**
- For EVERY candidate issue, run the existing-PR check and the assignee check BEFORE scoping work.
- A duplicate PR is low-value and reads as spam — it actively hurts reputation. The whole point of
  the system is *valued* contributions.
- Small, obvious bugs are the MOST likely to already have a PR (everyone grabs the easy ones).
  Weight triage toward slightly-less-obvious but still well-scoped issues that are genuinely unclaimed.

**Linked:** [[02-Repos/NousResearch__hermes-agent]] · playbook updated: `04-Playbooks/repo-triage.md`
(step 3 now bolds the existing-PR check).
