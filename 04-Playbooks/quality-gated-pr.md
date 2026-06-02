# Playbook: Quality-Gated PR

How to ship a contribution a maintainer will actually merge and appreciate.

## Steps

1. **Confirm scope.** You should have a precise spec: what change, why it adds value, exact files,
   and a test plan. If fuzzy, sharpen it before touching code.

2. **Read the repo's rules.** CONTRIBUTING.md, PR template, 3-5 recent MERGED PRs. Learn commit
   style, PR description format, DCO/sign-off needs, review etiquette. Match exactly.

3. **Fork + branch.**
   ```bash
   gh repo fork OWNER/REPO --clone=true   # or use existing fork
   cd REPO
   git checkout -b fix/short-descriptive-name      # NEVER work on default branch
   ```

4. **Implement (Brain directs, Worker executes mechanical parts).**
   - Brain writes the exact spec for each unit of work.
   - Delegate mechanical implementation to the Worker model (Hermes: `delegate_task`; Claude Code:
     a sub-task or Sonnet pass) with full context (file contents, signatures, conventions).
   - Brain does anything needing judgment (API design, naming, error handling).
   - **Brain reviews every returned diff against the spec + repo conventions. Redo weak parts.**

5. **Test for real (NEVER fabricate).** Find the project's test/lint command (CONTRIBUTING /
   package.json / Makefile / pyproject). Run it, capture real output, iterate until genuinely green.
   Add/adjust tests if the change warrants it.

6. **Self-review the full diff.** `git diff` — read every line. No scope creep, no debug prints,
   no unrelated changes, formatting matches.

7. **Commit (Brain writes the message).** Conventional style unless repo differs; `-s` if DCO required.
   ```bash
   git add -p
   git commit -m "fix: concise subject

   Body: what & why, references #NNN."
   ```

8. **Push + open PR (Brain writes the description).**
   ```bash
   git push -u origin fix/short-descriptive-name
   gh pr create --repo OWNER/REPO --title "..." --body "..."
   ```
   PR body: what, why, how tested, link to issue. Thoughtful, concise, human — follow their template.

9. **Record.** Capture PR URL → repo dossier + journal. Report to Telegram with the link.

10. **Follow up.** Watch CI + review. Respond promptly and graciously (Brain writes replies). Push
    fixes on the same branch.

## Quality bar (maintainer's checklist)

- Solves a real, scoped problem; zero unrelated churn.
- Tests pass (proven); new behavior covered.
- Matches project style & conventions.
- Clear commit + PR description; references the issue.
- Reads like a thoughtful human contribution, not AI bulk output.

## Pitfalls

- Worker models miss edge cases — Brain must verify.
- Don't open a PR before local CI-equivalent passes.
- Don't argue with maintainers; adapt to their preferences.
- If the change balloons beyond scope, split it.
