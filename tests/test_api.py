"""Unit tests for the GitHub API client (HTTP mocked with responses)."""

from __future__ import annotations

import time

import pytest
import requests
import responses

from github_rep import api
from github_rep.api import GitHubClient, RateLimitError


@pytest.fixture(autouse=True)
def _isolated_cache(tmp_path, monkeypatch):
    """Point the module cache dir at a throwaway path for every test."""
    monkeypatch.setattr(api, "CACHE_DIR", tmp_path)


@responses.activate
def test_auth_header_present_with_token():
    responses.add(responses.GET, "https://api.github.com/users/octocat",
                  json={"login": "octocat"}, status=200)
    GitHubClient(token="abc123").get_user("octocat")
    assert responses.calls[0].request.headers["Authorization"] == "Bearer abc123"


@responses.activate
def test_no_auth_header_without_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_PAT", raising=False)
    responses.add(responses.GET, "https://api.github.com/users/octocat",
                  json={"login": "octocat"}, status=200)
    GitHubClient().get_user("octocat")
    assert "Authorization" not in responses.calls[0].request.headers


@responses.activate
def test_rate_limit_403_raises():
    responses.add(responses.GET, "https://api.github.com/users/octocat",
                  json={"message": "API rate limit exceeded"}, status=403,
                  headers={"X-RateLimit-Reset": str(int(time.time()) + 60)})
    with pytest.raises(RateLimitError):
        GitHubClient().get_user("octocat")


@responses.activate
def test_rate_limit_429_secondary_raises():
    # GitHub secondary limits return 429 + Retry-After, not 403.
    responses.add(responses.GET, "https://api.github.com/users/octocat",
                  json={"message": "You have exceeded a secondary rate limit"},
                  status=429, headers={"Retry-After": "30"})
    with pytest.raises(RateLimitError):
        GitHubClient().get_user("octocat")


@responses.activate
def test_404_raises_http_error():
    responses.add(responses.GET, "https://api.github.com/users/ghost",
                  json={"message": "Not Found"}, status=404)
    with pytest.raises(requests.HTTPError):
        GitHubClient().get_user("ghost")


@responses.activate
def test_repeated_get_is_cached():
    responses.add(responses.GET, "https://api.github.com/users/octocat",
                  json={"login": "octocat"}, status=200)
    client = GitHubClient()
    client.get_user("octocat")
    client.get_user("octocat")  # second call served from cache
    assert len(responses.calls) == 1


@responses.activate
def test_get_repos_paginates_and_filters_forks():
    page1 = [{"name": f"r{i}", "fork": False} for i in range(100)]
    page2 = [{"name": "fork1", "fork": True}, {"name": "orig", "fork": False}]
    responses.add(responses.GET, "https://api.github.com/users/octocat/repos",
                  json=page1, status=200)
    responses.add(responses.GET, "https://api.github.com/users/octocat/repos",
                  json=page2, status=200)
    repos = GitHubClient().get_repos("octocat", include_forks=False)
    assert len(repos) == 101  # 100 + orig; the fork is filtered out
    assert all(not r["fork"] for r in repos)


@responses.activate
def test_get_repos_includes_forks_when_requested():
    responses.add(responses.GET, "https://api.github.com/users/octocat/repos",
                  json=[{"name": "fork1", "fork": True}, {"name": "orig", "fork": False}],
                  status=200)
    repos = GitHubClient().get_repos("octocat", include_forks=True)
    assert len(repos) == 2
