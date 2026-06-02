# github-rep

[![PyPI version](https://img.shields.io/pypi/v/github-rep.svg)](https://pypi.org/project/github-rep/)
[![Python versions](https://img.shields.io/pypi/pyversions/github-rep.svg)](https://pypi.org/project/github-rep/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Score any GitHub profile across 9 honest reputation signals and get a prioritized fix list — in under 30 seconds.**

---

## Install

```bash
pip install github-rep
```

Requires Python 3.9+. Dependencies: , ,                                                                                
 Usage: typer [OPTIONS] [PATH_OR_MODULE] COMMAND [ARGS]...                     
                                                                               
 Run Typer scripts with completion, without having to create a package.        
                                                                               
 You probably want to install completion for the typer command:                
                                                                               
 $ typer --install-completion                                                  
                                                                               
 https://typer.tiangolo.com/                                                   
                                                                               
+- Arguments -----------------------------------------------------------------+
|   path_or_module      [PATH_OR_MODULE]                                      |
+-----------------------------------------------------------------------------+
+- Options -------------------------------------------------------------------+
| --app                       TEXT  The typer app object/variable to use.     |
| --func                      TEXT  The function to convert to Typer.         |
| --version                         Print version and exit.                   |
| --install-completion              Install completion for the current shell. |
| --show-completion                 Show completion for the current shell, to |
|                                   copy it or customize the installation.    |
| --help                            Show this message and exit.               |
+-----------------------------------------------------------------------------+
+- Commands ------------------------------------------------------------------+
| utils  Extra utility commands for Typer apps.                               |
+-----------------------------------------------------------------------------+.

---

## Quickstart

```bash
export GITHUB_TOKEN=ghp_yourtoken   # optional but avoids rate limits
github-rep analyze-profile torvalds
```

Sample output:

```
╭──────────────────────── GitHub Profile ────────────────────────╮
│ @torvalds  |  Linus Torvalds                                    │
│ Linux and git                                                   │
│ Followers: 231,000  |  Public repos: 10  |  Stars earned: 232k │
╰─────────────────────────────────────────────────────────────────╯
Grade: A  (91/100)
Tier: Established authority

          Score Breakdown
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┓
┃ Dimension                ┃  Score ┃   Max ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━┩
│ Profile Completeness     │     10 │    10 │
│ Readme Quality           │     15 │    15 │
│ Star Signal              │     20 │    20 │
│ Contribution Streak      │     15 │    15 │
│ Repo Diversity           │      6 │    10 │
│ Description Quality      │      8 │    10 │
│ Topic Tags               │      4 │     5 │
│ Fork Ratio               │      5 │     5 │
│ Recent Activity          │      8 │    10 │
└──────────────────────────┴────────┴───────┘

Priority fixes:
  [MEDIUM] Only 10 public repos across 2 languages
```

---

## Scored dimensions

| Dimension | Max | What it measures |
|---|---|---|
| Profile Completeness | 10 | Name, bio, avatar, location, website |
| README Quality | 15 | Pinned profile README length and formatting |
| Star Signal | 20 | Stars earned (log-scaled, capped) |
| Contribution Streak | 15 | Recent commit frequency |
| Repo Diversity | 10 | Language breadth across repos |
| Description Quality | 10 | Repos with meaningful descriptions |
| Topic Tags | 5 | Repos tagged with relevant topics |
| Fork Ratio | 5 | Original work vs. forks |
| Recent Activity | 10 | Pushes and commits in last 90 days |

Scores are graded A (≥80) → B (≥65) → C (≥50) → D (≥35) → F.

---

## Why this exists

GitHub profiles are the de-facto developer resume. Most advice on building GitHub reputation is either
vague (just contribute more) or gameable (spam-stars, low-effort PRs). This tool measures the signals
that actually matter to recruiters, maintainers, and other developers — and tells you exactly what to fix
first, ordered by impact.

Built as a dogfood tool by [Hatchloop](https://hatchloop.dev/) while working on the
[GitHub reputation tracking service](https://hatchloop.dev/).

---

## Flags

```
github-rep analyze-profile <username> [--json] [--verbose]
```

| Flag | Description |
|---|---|
|  | Machine-readable JSON output |
|  | Show raw API data alongside scores |
|  | Print version and exit |

---

## Contributing

Bug reports and improvements welcome — open an issue on
[github.com/basilalshukaili/github-rep](https://github.com/basilalshukaili/github-rep/issues).

---

## License

MIT — see [LICENSE](LICENSE).
