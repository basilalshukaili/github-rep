# Changelog

All notable changes to github-rep are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.2.0] - 2026-06-02

### Added
- **New signal: Release Cadence (5 pts)** — scores whether the user publishes
  versioned GitHub Releases on their top repos. Published releases signal a
  production-ready, actively maintained project.
- **New signal: Profile README (5 pts)** — scores the presence and quality of
  the special `username/username` profile README, which is displayed to every
  profile visitor. Short README = 2 pts; substantial (100+ words) = 5 pts.
- **CONTRIBUTING.md** — development setup, contribution guidelines, and PR checklist.
- **Issue and PR templates** under `.github/`.
- **7 new pytest tests** covering both new signals across all score paths.

### Changed
- Total dimensions: 9 → 11 (max score still 100 pts via rebalanced weights).
- `analyze()` docstring updated to reflect 11 dimensions.
- `DIMENSION_MAX` dict in CLI is now the single source of truth for all dimension
  max values, used by both `analyze-profile` and `compare` commands.
- Sample output in README updated from fabricated to real (torvalds, 2026-06-02).
- README rewritten: clearer value prop, accurate badge block, JSON output example,
  expanded FAQ, all 11 dimensions documented.
- `__init__.py` version string updated to `0.2.0`.

### Fixed
- `compare` command now includes the two new dimensions in the side-by-side table.
- README dependencies section had garbled text from a typer help injection; removed.

---

## [0.1.1] - 2026-05-31

### Changed
- README polished with badges, quickstart, and real sample output.
- Correct PyPI and GitHub URLs.

---

## [0.1.0] - 2026-05-30

### Added
- Initial release with 9 reputation signals.
- `analyze-profile`, `compare`, and `rate-limit` CLI commands.
- GitHub API client with 5-minute cache and rate-limit awareness.
- CI workflow running tests on Python 3.9–3.12.
