"""Unit tests for the analyzer module (no network calls - all mocked)."""

from __future__ import annotations

from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch
import base64

import pytest

from github_rep.analyzer import (
    Finding,
    ProfileScore,
    _days_since,
    _readme_score,
    analyze,
)
from github_rep.api import GitHubClient


# -- Helpers -------------------------------------------------------------------

def _dt(days_ago: int) -> str:
    dt = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return dt.isoformat().replace("+00:00", "Z")


def _make_user(**kwargs) -> dict:
    defaults = {
        "login": "testuser",
        "name": "Test User",
        "bio": "I build things.",
        "location": "Earth",
        "blog": "https://example.com",
        "company": "Acme",
        "email": "test@example.com",
        "avatar_url": "https://avatars.githubusercontent.com/u/123",
        "followers": 10,
        "public_repos": 5,
        "updated_at": _dt(5),
        "twitter_username": None,
    }
    defaults.update(kwargs)
    return defaults


def _make_repo(name: str = "my-repo", stars: int = 10, fork: bool = False,
               description: str = "A repo", topics=None, days_ago: int = 3) -> dict:
    return {
        "name": name,
        "stargazers_count": stars,
        "fork": fork,
        "description": description,
        "topics": topics or ["python", "cli"],
        "language": "Python",
        "pushed_at": _dt(days_ago),
    }


# -- _days_since ---------------------------------------------------------------

class TestDaysSince:
    def test_none_returns_none(self):
        assert _days_since(None) is None

    def test_recent(self):
        assert _days_since(_dt(3)) == 3

    def test_old(self):
        assert _days_since(_dt(200)) == 200

    def test_malformed(self):
        assert _days_since("not-a-date") is None


# -- _readme_score -------------------------------------------------------------

class TestReadmeScore:
    def test_no_readme_returns_zero_critical(self):
        score, findings = _readme_score(None)
        assert score == 0
        assert len(findings) == 1
        assert findings[0].severity == "critical"
        assert findings[0].title == "No README"

    def test_short_readme(self):
        readme = "A short readme."
        score, findings = _readme_score(readme)
        assert score <= 5
        severities = {f.severity for f in findings}
        assert "high" in severities

    def test_good_readme_with_code(self):
        readme = " ".join(["word"] * 200) + "\n```python\nprint('hello')\n```\npip install foo"
        score, findings = _readme_score(readme)
        assert score >= 12
        good_or_none = all(f.severity not in ("critical", "high") for f in findings)
        assert good_or_none

    def test_max_score_cap(self):
        readme = " ".join(["word"] * 500) + "\n```code```\npip install foo"
        score, _ = _readme_score(readme)
        assert score <= 15


# -- Finding -------------------------------------------------------------------

class TestFinding:
    @pytest.mark.parametrize("severity,expected", [
        ("critical", "[CRITICAL]"),
        ("good",     "[GOOD]"),
        ("medium",   "[MEDIUM]"),
    ])
    def test_icon(self, severity, expected):
        f = Finding("cat", severity, "title", "detail")
        assert f.icon == expected


# -- ProfileScore --------------------------------------------------------------

class TestProfileScore:
    @pytest.mark.parametrize("total,grade", [
        (85, "A"), (70, "B"), (55, "C"), (40, "D"), (20, "F"),
    ])
    def test_grade(self, total, grade):
        s = ProfileScore("u", total)
        assert s.grade == grade

    @pytest.mark.parametrize("total,tier", [
        (90, "Established OSS contributor"),
        (65, "Active developer"),
        (50, "Growing presence"),
        (35, "Early stage"),
        (10, "Just starting"),
    ])
    def test_tier(self, total, tier):
        s = ProfileScore("u", total)
        assert s.tier == tier


# -- Full analyze() with mocked API --------------------------------------------

class TestAnalyze:
    def _mock_client(self, user, repos, readme_content=None,
                     releases=None, profile_readme=None):
        """Return a mock GitHubClient."""
        client = MagicMock(spec=GitHubClient)
        client.get_user.return_value = user
        client.get_repos.side_effect = lambda username, include_forks=False: (
            repos + [_make_repo("forked", fork=True)] if include_forks else repos
        )

        def mock_get(path, params=None, **kwargs):
            if "/readme" in path:
                # Profile README (username/username)
                parts = path.split("/")
                if len(parts) >= 4 and parts[2] == parts[3]:
                    if profile_readme is None:
                        raise Exception("404 Not Found")
                    return {"content": base64.b64encode(profile_readme.encode()).decode()}
                # Repo README
                if readme_content is None:
                    raise Exception("404 Not Found")
                return {"content": base64.b64encode(readme_content.encode()).decode()}
            if "/releases" in path:
                return releases if releases is not None else []
            return {}

        client.get.side_effect = mock_get
        return client

    @patch("github_rep.analyzer.GitHubClient")
    def test_high_score_complete_profile(self, MockClient):
        user = _make_user()
        repos = [_make_repo(f"repo-{i}", stars=50) for i in range(12)]
        readme = " ".join(["word"] * 200) + "\n```python\nprint('hi')\n```\npip install foo"
        MockClient.return_value = self._mock_client(user, repos, readme)

        score = analyze("testuser")

        assert score.total > 60
        assert score.grade in ("A", "B", "C")
        assert score.username == "testuser"
        assert "profile_completeness" in score.breakdown

    @patch("github_rep.analyzer.GitHubClient")
    def test_low_score_empty_profile(self, MockClient):
        user = _make_user(bio=None, location=None, blog=None,
                          company=None, email=None, avatar_url="",
                          updated_at=_dt(365))
        repos = []
        MockClient.return_value = self._mock_client(user, repos)

        score = analyze("emptyuser")

        assert score.total < 40
        assert score.grade in ("D", "F")
        severities = {f.severity for f in score.findings}
        assert "critical" in severities or "high" in severities

    @patch("github_rep.analyzer.GitHubClient")
    def test_findings_sorted_by_severity(self, MockClient):
        user = _make_user(bio=None)
        repos = [_make_repo()]
        MockClient.return_value = self._mock_client(user, repos)

        score = analyze("testuser")

        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "good": 4}
        orders = [severity_order.get(f.severity, 5) for f in score.findings]
        assert orders == sorted(orders)

    @patch("github_rep.analyzer.GitHubClient")
    def test_breakdown_sums_to_total(self, MockClient):
        user = _make_user()
        repos = [_make_repo()]
        MockClient.return_value = self._mock_client(user, repos)

        score = analyze("testuser")

        assert sum(score.breakdown.values()) == score.total

    @patch("github_rep.analyzer.GitHubClient")
    def test_zero_stars_finding(self, MockClient):
        user = _make_user()
        repos = [_make_repo(stars=0)]
        MockClient.return_value = self._mock_client(user, repos)

        score = analyze("testuser")
        star_findings = [f for f in score.findings if f.category == "star_signal"]
        assert any(f.severity in ("high", "medium") for f in star_findings)

    # -- New signal: release_cadence -------------------------------------------

    @patch("github_rep.analyzer.GitHubClient")
    def test_release_cadence_no_releases(self, MockClient):
        user = _make_user()
        repos = [_make_repo()]
        MockClient.return_value = self._mock_client(user, repos, releases=[])

        score = analyze("testuser")

        assert "release_cadence" in score.breakdown
        assert score.breakdown["release_cadence"] == 0
        rc_findings = [f for f in score.findings if f.category == "release_cadence"]
        assert len(rc_findings) == 1
        assert rc_findings[0].severity == "low"

    @patch("github_rep.analyzer.GitHubClient")
    def test_release_cadence_few_releases(self, MockClient):
        user = _make_user()
        repos = [_make_repo()]
        fake_releases = [{"tag_name": "v0.1.0"}, {"tag_name": "v0.2.0"}]
        MockClient.return_value = self._mock_client(user, repos, releases=fake_releases)

        score = analyze("testuser")

        assert score.breakdown["release_cadence"] == 3
        rc_findings = [f for f in score.findings if f.category == "release_cadence"]
        assert rc_findings[0].severity == "low"

    @patch("github_rep.analyzer.GitHubClient")
    def test_release_cadence_many_releases(self, MockClient):
        user = _make_user()
        repos = [_make_repo(f"repo-{i}") for i in range(5)]
        # Each of 5 repos has 1 release = 5 total (>= 3 threshold)
        fake_releases = [{"tag_name": "v1.0.0"}]
        MockClient.return_value = self._mock_client(user, repos, releases=fake_releases)

        score = analyze("testuser")

        assert score.breakdown["release_cadence"] == 5
        rc_findings = [f for f in score.findings if f.category == "release_cadence"]
        assert rc_findings[0].severity == "good"

    # -- New signal: profile_readme --------------------------------------------

    @patch("github_rep.analyzer.GitHubClient")
    def test_profile_readme_missing(self, MockClient):
        user = _make_user()
        repos = [_make_repo()]
        MockClient.return_value = self._mock_client(user, repos, profile_readme=None)

        score = analyze("testuser")

        assert "profile_readme" in score.breakdown
        assert score.breakdown["profile_readme"] == 0
        pr_findings = [f for f in score.findings if f.category == "profile_readme"]
        assert len(pr_findings) == 1
        assert pr_findings[0].severity == "medium"

    @patch("github_rep.analyzer.GitHubClient")
    def test_profile_readme_short(self, MockClient):
        user = _make_user()
        repos = [_make_repo()]
        short_readme = "Hi I code things."
        MockClient.return_value = self._mock_client(user, repos, profile_readme=short_readme)

        score = analyze("testuser")

        assert score.breakdown["profile_readme"] == 2
        pr_findings = [f for f in score.findings if f.category == "profile_readme"]
        assert pr_findings[0].severity == "low"

    @patch("github_rep.analyzer.GitHubClient")
    def test_profile_readme_substantial(self, MockClient):
        user = _make_user()
        repos = [_make_repo()]
        long_readme = " ".join(["word"] * 150)
        MockClient.return_value = self._mock_client(user, repos, profile_readme=long_readme)

        score = analyze("testuser")

        assert score.breakdown["profile_readme"] == 5
        pr_findings = [f for f in score.findings if f.category == "profile_readme"]
        assert pr_findings[0].severity == "good"

    @patch("github_rep.analyzer.GitHubClient")
    def test_breakdown_has_all_11_dimensions(self, MockClient):
        user = _make_user()
        repos = [_make_repo()]
        MockClient.return_value = self._mock_client(user, repos)

        score = analyze("testuser")

        expected_dims = {
            "profile_completeness", "readme_quality", "star_signal",
            "contribution_streak", "repo_diversity", "description_quality",
            "topic_tags", "fork_ratio", "recent_activity",
            "release_cadence", "profile_readme",
        }
        assert set(score.breakdown.keys()) == expected_dims
