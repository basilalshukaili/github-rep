"""Tests for the CLI commands (analyze logic mocked, no network)."""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import patch

from typer.testing import CliRunner

from github_rep.api import RateLimitError
from github_rep.cli import app

runner = CliRunner()


def _fake_score():
    return SimpleNamespace(
        username="octocat",
        total=85,
        grade="A",
        tier="Established OSS contributor",
        breakdown={"profile_completeness": 10, "star_signal": 20},
        findings=[],
        raw_user={"name": "Octo", "bio": "", "followers": 1, "public_repos": 2},
        raw_repos=[],
    )


@patch("github_rep.cli.analyze")
def test_analyze_profile_json_output(mock_analyze):
    mock_analyze.return_value = _fake_score()
    result = runner.invoke(app, ["analyze-profile", "octocat", "--json"])
    assert result.exit_code == 0
    out = result.stdout
    data = json.loads(out[out.index("{"):out.rindex("}") + 1])
    assert data["username"] == "octocat"
    assert data["total"] == 85
    assert data["grade"] == "A"


@patch("github_rep.cli.analyze")
def test_analyze_profile_rate_limit_exits_1(mock_analyze):
    mock_analyze.side_effect = RateLimitError("Rate limited. Resets soon.")
    result = runner.invoke(app, ["analyze-profile", "octocat"])
    assert result.exit_code == 1
    assert "Rate limit hit" in result.stdout


@patch("github_rep.cli.analyze")
def test_analyze_profile_generic_error_exits_1(mock_analyze):
    mock_analyze.side_effect = ValueError("boom")
    result = runner.invoke(app, ["analyze-profile", "octocat"])
    assert result.exit_code == 1


def test_compare_requires_two_usernames():
    result = runner.invoke(app, ["compare", "onlyone"])
    assert result.exit_code == 1
    assert "at least 2" in result.stdout
