# github-rep

[![PyPI version](https://img.shields.io/pypi/v/github-rep.svg)](https://pypi.org/project/github-rep/)
[![Python versions](https://img.shields.io/pypi/pyversions/github-rep.svg)](https://pypi.org/project/github-rep/)
[![CI](https://github.com/basilalshukaili/github-rep/actions/workflows/ci.yml/badge.svg)](https://github.com/basilalshukaili/github-rep/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Score any GitHub user's reputation across 11 honest signals and get a prioritized fix list — in under 30 seconds.**

---

## Why this exists

GitHub profiles are the de-facto developer resume. Most advice on building GitHub reputation is either
vague ("just contribute more") or gameable (spam-stars, low-effort PRs). This tool measures the signals
that actually matter to recruiters, maintainers, and other developers — and tells you exactly what to
fix first, ordered by impact.

---

## Install

```bash
pip install github-rep
```

Requires Python 3.9+. No configuration needed — works unauthenticated (60 req/hr) or with a GitHub
token for 5000 req/hr.

---

## Quickstart

```bash
# Analyze any GitHub user
github-rep analyze-profile torvalds

# Use a token to avoid rate limits
export GITHUB_TOKEN=ghp_yourtoken
github-rep analyze-profile sindresorhus

# Machine-readable JSON output
github-rep analyze-profile gvanrossum --json

# Show all findings, including low-priority ones
github-rep analyze-profile octocat --verbose

# Compare multiple profiles side by side
github-rep compare torvalds gvanrossum sindresorhus

# Check your API rate limit
github-rep rate-limit
```

---

## Sample output

```
$ github-rep analyze-profile torvalds

╭──────────────────────────────── GitHub Profile ─────────────────────────────╮
│ @torvalds  |  Linus Torvalds                                                │
│                                                                              │
│ Followers: 305,509  |  Public repos: 12  |  Stars earned: 246,028           │
╰──────────────────────────────────────────────────────────────────────────────╯
Grade: B  (78/100)
Tier: Active developer

                Score Breakdown
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ Dimension                ┃  Score ┃   Max ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ Profile Completeness     │      4 │    10 │
│ Readme Quality           │     12 │    15 │
│ Star Signal              │     20 │    20 │
│ Contribution Streak      │     15 │    15 │
│ Repo Diversity           │      7 │    10 │
│ Description Quality      │     10 │    10 │
│ Topic Tags               │      0 │     5 │
│ Fork Ratio               │      5 │     5 │
│ Recent Activity          │      5 │    10 │
│ Release Cadence          │      0 │     5 │
│ Profile Readme           │      0 │     5 │
└──────────────────────────┴────────┴───────┘

Priority fixes:
  [HIGH] Missing bio
     Your bio is empty. It is the first thing visitors read.
     Fix: Write 1-2 sentences: your focus, what you build, your superpower.

What is working:
  [GOOD] Strong star signal (246028 total, top repo: 235147)
  [GOOD] Active recent commits (0d ago)
  [GOOD] All repos have descriptions
```

Grades: **A** (≥80) · **B** (≥65) · **C** (≥50) · **D** (≥35) · **F**

---

## The 11 scored dimensions

| # | Dimension | Max pts | What it measures |
|---|-----------|--------:|------------------|
| 1 | Profile Completeness | 10 | Name, bio, avatar, location, website / social link |
| 2 | README Quality | 15 | Top repo README length, code examples, install instructions |
| 3 | Star Signal | 20 | Total stars earned across all repos (log-scaled) |
| 4 | Contribution Streak | 15 | Days since last profile activity |
| 5 | Repo Diversity | 10 | Number of public repos and language breadth |
| 6 | Description Quality | 10 | Fraction of repos with meaningful descriptions |
| 7 | Topic Tags | 5 | Repos tagged with relevant GitHub topics |
| 8 | Fork Ratio | 5 | Proportion of original work vs. forked repos |
| 9 | Recent Activity | 10 | Repos with pushes in the last 90 days |
| 10 | **Release Cadence** | 5 | Published GitHub Releases on top repos |
| 11 | **Profile README** | 5 | Presence and quality of the username/username profile README |

**Total: 100 points.**

Dimensions 10 and 11 are new in v0.2.0 and measure signals that indicate a polished,
production-ready presence — publishing versioned releases and curating a profile page.

---

## All flags

```
github-rep analyze-profile <username> [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--json` | Machine-readable JSON output (all scores + findings) |
| `--verbose` / `-v` | Show all findings including low-priority improvements |
| `--token` / `-t` | GitHub PAT (also reads `GITHUB_TOKEN` env var) |
| `--top N` | Number of top repos to deep-analyze (default: 10) |
| `--help` | Show help and exit |

---

## JSON output

```bash
github-rep analyze-profile gvanrossum --json
```

```json
{
  "username": "gvanrossum",
  "total": 72,
  "grade": "B",
  "tier": "Active developer",
  "breakdown": {
    "profile_completeness": 8,
    "readme_quality": 12,
    ...
  },
  "findings": [
    {
      "category": "topic_tags",
      "severity": "medium",
      "title": "Most repos have no topic tags",
      "detail": "Missing from GitHub Explore category pages entirely.",
      "fix": "Add topics to your top 3 repos today - GitHub UI, takes 2 minutes."
    }
  ]
}
```

---

## Caching

Results are cached for 5 minutes under `~/.cache/github-rep/` to avoid hitting rate limits when
running the tool multiple times. Delete the cache directory to force a fresh fetch.

---

## FAQ

**Do I need a GitHub token?**
No. Unauthenticated usage gets 60 API requests per hour — enough for a single profile analysis.
Set `GITHUB_TOKEN` to get 5000 requests per hour and avoid hitting limits when comparing many profiles.

**How is the score calculated?**
Each dimension is scored independently against fixed max points (totalling 100). There is no
machine learning or relative ranking — the score reflects the absolute presence or absence of
each signal.

**Can I game the score?**
You could game every individual metric, but you would also genuinely improve your GitHub presence
in the process. The signals are chosen because they correlate with real reputation value.

**Why does a well-known developer score lower than expected?**
Some high-reputation developers (including Linus Torvalds) score below 80 because they skip
signals like topic tags, profile READMEs, or GitHub Releases. The tool measures profile
hygiene signals, not absolute influence.

**How often should I re-run this?**
After each batch of improvements. Treat it like `npm audit` — run it, fix the findings, move on.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports and improvements welcome — open an issue on
[github.com/basilalshukaili/github-rep](https://github.com/basilalshukaili/github-rep/issues).

---

## License

MIT — see [LICENSE](LICENSE).
