# Contributing to github-rep

Thank you for considering a contribution. This document covers how to get set up,
what kinds of contributions are most useful, and how to submit a pull request.

---

## Development setup

```bash
git clone https://github.com/basilalshukaili/github-rep.git
cd github-rep
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Run the tests:

```bash
pytest tests/ -v
```

Run the CLI against a real account (requires a GitHub token for best results):

```bash
export GITHUB_TOKEN=ghp_yourtoken
github-rep analyze-profile torvalds
```

---

## What makes a good contribution

**High value:**
- A new scoring dimension with a clear reputation rationale, a max of 5-10 pts, and tests
- Bug fixes for incorrect scoring logic
- Better error messages or rate-limit handling
- Performance improvements to the API client

**Low value (likely to be declined):**
- Padding existing scores upward without signal justification
- Dependencies that add significant install weight
- Style changes without functional improvement

---

## Adding a new scoring dimension

1. Implement it in `src/github_rep/analyzer.py` — add it to `breakdown` with a max score
2. Add the dimension to `DIMENSION_MAX` in `src/github_rep/cli.py`
3. Write at least two pytest tests (one for the low-score path, one for the high-score path)
4. Update the dimensions table in `README.md`
5. Bump the minor version in `pyproject.toml` and `src/github_rep/__init__.py`
6. Add a CHANGELOG entry

---

## Pull request checklist

- [ ] `pytest tests/ -v` passes with no failures
- [ ] New behavior has test coverage
- [ ] README updated if a user-visible change was made
- [ ] CHANGELOG entry added under `[Unreleased]`
- [ ] Version bumped if the change is user-visible

---

## Reporting bugs

Open an issue at [github.com/basilalshukaili/github-rep/issues](https://github.com/basilalshukaili/github-rep/issues).
Include: the username you analyzed, the error or unexpected output, your Python version, and
whether you used a token.
