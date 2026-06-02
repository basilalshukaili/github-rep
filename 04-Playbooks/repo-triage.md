# Playbook: Repo Triage

Goal: understand a target repo well enough to add real value, and find the RIGHT unclaimed thing
to work on. Produces/updates a dossier in `02-Repos/<owner>__<repo>.md`.

## Steps

1. **Survey the repo.**
   - `gh repo view OWNER/REPO --json name,description,stargazerCount,primaryLanguage,licenseInfo`
   - Read README, CONTRIBUTING.md, CODE_OF_CONDUCT.md, docs/ARCHITECTURE.
   - Check for any AI-PR policy. If AI contributions are disallowed → STOP, pick another repo.
   - Note the exact test command, CI setup, language(s), lint/format tooling.

2. **Read the room.**
   - Recent MERGED PRs: `gh pr list --repo OWNER/REPO --state merged --limit 20` — learn what
     gets merged, by whom, size, commit/PR style.
   - Open PRs: what's already in flight (so you don't duplicate).
   - Maintainer responsiveness & tone.

3. **Find UNCLAIMED opportunities (ranked by value × tractability).**
   - `gh issue list --repo OWNER/REPO --state open --limit 40 --json number,title,labels,assignees`
   - Prefer type/bug with P2/P3, small docs gaps, failing/flaky tests, missing edge-case handling,
     platform quirks (Windows knowledge is a strong niche).
   - **CRITICAL: for every candidate, confirm there is NO existing open PR and NO assignee:**
     `gh pr list --repo OWNER/REPO --state open --search "<issue-number>"`
     Also search PR titles for related keywords. If a PR already addresses it → SKIP. A duplicate
     PR is low-value and looks like spam — it hurts reputation.
   - AVOID: huge features, RFCs, contentious design debates, vague issues, assigned issues.

4. **Validate locally.** Clone, build, run tests. Reproduce the bug you intend to fix. Confirm you
   can make the change cleanly before committing to it.

5. **Write the dossier** → `02-Repos/<owner>__<repo>.md` (use `_TEMPLATE.md`): stack, exact test
   command, conventions, maintainer notes, candidate issues (links + your assessment + PR-exists
   check), and the ONE you'll tackle first.

## Pitfalls

- The #1 mistake is picking an issue that already has an open PR. ALWAYS check first.
- If you can't reproduce a bug, you can't credibly fix it.
- Claim an issue with a comment (Brain writes it) only when you're ready to work it, per repo norms.
