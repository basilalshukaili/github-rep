"""GitHub API client with rate-limit awareness and caching."""

import time
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

GITHUB_API = "https://api.github.com"
CACHE_DIR = Path.home() / ".cache" / "github-rep"


class RateLimitError(Exception):
    pass


class GitHubClient:
    """Thin wrapper around the GitHub REST API v3.

    Supports both authenticated and unauthenticated usage.
    Unauthenticated: 60 req/hr  |  Authenticated: 5000 req/hr
    """

    def __init__(self, token: Optional[str] = None, cache_ttl: int = 300):
        self.token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_PAT")
        self.cache_ttl = cache_ttl
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "github-rep/0.2.0",
        })
        if self.token:
            self.session.headers["Authorization"] = f"Bearer {self.token}"
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _cache_key(self, url: str, params: dict) -> Path:
        key = hashlib.md5(f"{url}{json.dumps(params, sort_keys=True)}".encode()).hexdigest()
        return CACHE_DIR / f"{key}.json"

    def _get_cached(self, url: str, params: dict) -> Optional[Any]:
        cache_file = self._cache_key(url, params)
        if cache_file.exists():
            age = time.time() - cache_file.stat().st_mtime
            if age < self.cache_ttl:
                return json.loads(cache_file.read_text())
        return None

    def _set_cached(self, url: str, params: dict, data: Any) -> None:
        cache_file = self._cache_key(url, params)
        cache_file.write_text(json.dumps(data))

    def get(self, path: str, params: Optional[Dict] = None, use_cache: bool = True) -> Any:
        params = params or {}
        url = f"{GITHUB_API}{path}"
        if use_cache:
            cached = self._get_cached(url, params)
            if cached is not None:
                return cached
        resp = self.session.get(url, params=params)
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset = int(resp.headers.get("X-RateLimit-Reset", 0))
            raise RateLimitError(f"Rate limited. Resets at {time.ctime(reset)}")
        resp.raise_for_status()
        data = resp.json()
        if use_cache:
            self._set_cached(url, params, data)
        return data

    def get_user(self, username: str) -> Dict:
        return self.get(f"/users/{username}")

    def get_repos(self, username: str, include_forks: bool = False) -> List[Dict]:
        repos = []
        page = 1
        while True:
            batch = self.get(f"/users/{username}/repos",
                             params={"per_page": 100, "page": page, "sort": "updated"})
            if not batch:
                break
            repos.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        if not include_forks:
            repos = [r for r in repos if not r["fork"]]
        return repos

    def get_repo(self, owner: str, repo: str) -> Dict:
        return self.get(f"/repos/{owner}/{repo}")

    def get_contributors(self, owner: str, repo: str) -> List[Dict]:
        try:
            return self.get(f"/repos/{owner}/{repo}/contributors", params={"per_page": 30})
        except Exception:
            return []

    def rate_limit_status(self) -> Dict:
        return self.get("/rate_limit", use_cache=False)
