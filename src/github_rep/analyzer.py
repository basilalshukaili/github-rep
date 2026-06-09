"""Profile analyzer: scores genuine reputation signals across 11 dimensions."""

from __future__ import annotations

import base64
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from .api import GitHubClient


@dataclass
class Finding:
    """A single scored observation about a GitHub profile."""

    category: str
    severity: str   # "critical" | "high" | "medium" | "low" | "good"
    title: str
    detail: str
    fix: Optional[str] = None

    @property
    def icon(self) -> str:
        return {
            "critical": "[CRITICAL]",
            "high":     "[HIGH]",
            "medium":   "[MEDIUM]",
            "low":      "[LOW]",
            "good":     "[GOOD]",
        }.get(self.severity, "[?]")


@dataclass
class ProfileScore:
    """Complete reputation analysis for one GitHub user."""

    username: str
    total: int                            # 0-100
    breakdown: Dict[str, int] = field(default_factory=dict)
    findings: List[Finding] = field(default_factory=list)
    raw_user: Dict = field(default_factory=dict)
    raw_repos: List[Dict] = field(default_factory=list)

    @property
    def grade(self) -> str:
        if self.total >= 80:
            return "A"
        if self.total >= 65:
            return "B"
        if self.total >= 50:
            return "C"
        if self.total >= 35:
            return "D"
        return "F"

    @property
    def tier(self) -> str:
        if self.total >= 80:
            return "Established OSS contributor"
        if self.total >= 65:
            return "Active developer"
        if self.total >= 50:
            return "Growing presence"
        if self.total >= 35:
            return "Early stage"
        return "Just starting"


# -- Helpers -------------------------------------------------------------------

def _days_since(dt_str: Optional[str]) -> Optional[int]:
    if not dt_str:
        return None
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return None


def _readme_score(readme_text: Optional[str]) -> Tuple[int, List[Finding]]:
    """Score README quality 0-15 and return relevant findings."""
    findings: List[Finding] = []

    if not readme_text:
        return 0, [Finding(
            "readme_quality", "critical",
            "No README",
            "Your repo has no README. This is the #1 reason developers skip a project.",
            "Add README.md: what it does, why it matters, how to install, quick example.",
        )]

    score = 0
    words = len(readme_text.split())

    if words < 50:
        findings.append(Finding(
            "readme_quality", "high",
            "README too short",
            f"Only {words} words. A useful README is 150-500 words.",
            "Add: what it does, installation, usage example, screenshot.",
        ))
        score += 3
    elif words < 150:
        score += 7
        findings.append(Finding(
            "readme_quality", "medium",
            "README could be richer",
            f"{words} words - decent, but consider adding usage examples.",
            "Add a code example or screenshot to make it concrete.",
        ))
    else:
        score += 12

    if "```" in readme_text or "`" in readme_text:
        score += 2
    else:
        findings.append(Finding(
            "readme_quality", "medium",
            "No code examples",
            "README has no inline code. Show, do not just tell.",
            "Add a quick-start code block showing the most common use case.",
        ))

    has_install = any(
        kw in readme_text.lower()
        for kw in ["install", "pip install", "npm install", "brew install", "cargo add"]
    )
    if has_install:
        score += 1
    else:
        findings.append(Finding(
            "readme_quality", "low",
            "No installation instructions",
            "How should someone install this?",
            'Add an "## Installation" section even if it is just `pip install <name>`.',
        ))

    return min(score, 15), findings


# -- Main analyzer -------------------------------------------------------------

def analyze(
    username: str,
    token: Optional[str] = None,
    top_n: int = 10,
) -> ProfileScore:
    """Fetch GitHub data and compute a ProfileScore across 11 dimensions.

    Args:
        username:  GitHub username to analyze.
        token:     Optional GitHub personal access token (improves rate limits).
        top_n:     Number of top repos (by stars) to deep-analyze.

    Returns:
        ProfileScore with total (0-100), breakdown, and actionable findings.
    """
    client = GitHubClient(token=token)
    user = client.get_user(username)
    all_repos = client.get_repos(username, include_forks=True)
    repos = [r for r in all_repos if not r.get("fork")]
    repos_sorted = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)
    top_repos = repos_sorted[:top_n]

    breakdown: Dict[str, int] = {}
    findings: List[Finding] = []

    # 1. Profile completeness (10 pts) ----------------------------------------
    pc = 0
    if user.get("bio"):
        pc += 3
    else:
        findings.append(Finding(
            "profile_completeness", "high",
            "Missing bio",
            "Your bio is empty. It is the first thing visitors read.",
            "Write 1-2 sentences: your focus, what you build, your superpower.",
        ))
    if user.get("location"):
        pc += 1
    else:
        findings.append(Finding(
            "profile_completeness", "low",
            "No location set",
            "Location builds trust and helps local dev communities find you.",
            "Add your city/country - takes 5 seconds.",
        ))
    if user.get("blog") or user.get("twitter_username"):
        pc += 2
    else:
        findings.append(Finding(
            "profile_completeness", "medium",
            "No website or social link",
            "No linked website or Twitter/X. Credibility builder.",
            "Add your website, LinkedIn, or Twitter handle.",
        ))
    if user.get("company"):
        pc += 1
    if user.get("email"):
        pc += 1
    avatar = user.get("avatar_url", "")
    if avatar and "gravatar" not in avatar:
        pc += 2
    else:
        findings.append(Finding(
            "profile_completeness", "low",
            "Default/gravatar avatar",
            "A real photo or custom avatar increases perceived legitimacy.",
            "Upload a profile photo - even a simple avatar is better than the default.",
        ))
    breakdown["profile_completeness"] = min(pc, 10)

    # 2. README quality (15 pts) -----------------------------------------------
    readme_text: Optional[str] = None
    if top_repos:
        best = top_repos[0]
        try:
            raw = client.get(f"/repos/{username}/{best['name']}/readme")
            readme_text = base64.b64decode(raw["content"]).decode("utf-8", errors="replace")
        except Exception:
            readme_text = None
    readme_pts, readme_findings = _readme_score(readme_text)
    breakdown["readme_quality"] = readme_pts
    findings.extend(readme_findings)

    # 3. Star signal (20 pts) --------------------------------------------------
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    max_stars = max((r.get("stargazers_count", 0) for r in repos), default=0)
    if total_stars == 0:
        star_pts = 0
        findings.append(Finding(
            "star_signal", "high",
            "Zero stars across all repos",
            "Stars are the #1 public signal of value. Zero usually means: "
            "no promotion, poor README, or no unique value prop.",
            "Fix the README, then share the project genuinely in ONE relevant community.",
        ))
    elif total_stars < 5:
        star_pts = 4
        findings.append(Finding(
            "star_signal", "medium",
            f"Low star count ({total_stars} total)",
            "Genuine stars come from genuine visibility.",
            "Share in community when you have something useful to say.",
        ))
    elif total_stars < 25:
        star_pts = 10
    elif total_stars < 100:
        star_pts = 15
    elif total_stars < 500:
        star_pts = 18
    else:
        star_pts = 20
        findings.append(Finding(
            "star_signal", "good",
            f"Strong star signal ({total_stars} total, top repo: {max_stars})",
            "Real community traction. Keep shipping.",
        ))
    breakdown["star_signal"] = star_pts

    # 4. Contribution activity (15 pts) ----------------------------------------
    # Honest signal: last push to an owned repo (real code activity), NOT the
    # profile's updated_at — which also bumps on stars, follows, and bio edits.
    last_push = max((r.get("pushed_at") for r in repos if r.get("pushed_at")), default=None)
    days = _days_since(last_push)
    if days is None or days > 180:
        streak_pts = 0
        findings.append(Finding(
            "contribution_streak", "high",
            "No recent activity (6+ months)",
            "Stale profiles are invisible in GitHub search and Explore.",
            "Even small commits (docs, tests, fixes) signal an active developer.",
        ))
    elif days > 60:
        streak_pts = 5
        findings.append(Finding(
            "contribution_streak", "medium",
            f"Low recent activity ({days} days since last push)",
            "Aim for a few commits per month to stay visible.",
            "Pick one project and make a small meaningful improvement weekly.",
        ))
    elif days > 14:
        streak_pts = 10
    else:
        streak_pts = 15
        findings.append(Finding(
            "contribution_streak", "good",
            f"Active recently (last push {days}d ago)",
            "Consistent shipping builds reputation over time.",
        ))
    breakdown["contribution_streak"] = streak_pts

    # 5. Repo diversity (10 pts) -----------------------------------------------
    n_repos = len(repos)
    if n_repos == 0:
        div_pts = 0
        findings.append(Finding(
            "repo_diversity", "critical",
            "No public repositories",
            "Nothing to discover, nothing to star, nothing to learn from.",
            "Publish at least one genuine project - even a small tool that solves a real problem.",
        ))
    elif n_repos < 3:
        div_pts = 3
        findings.append(Finding(
            "repo_diversity", "medium",
            f"Only {n_repos} public repos",
            "A single repo limits discovery surface. Build in public.",
            "Start a second project - even a CLI tool, a library, or documented configs.",
        ))
    elif n_repos < 10:
        div_pts = 7
    else:
        div_pts = 10
        languages = {r["language"] for r in repos if r.get("language")}
        if len(languages) >= 3:
            findings.append(Finding(
                "repo_diversity", "good",
                f"{n_repos} repos across {len(languages)} languages",
                "Healthy breadth. Visitors can see range and depth.",
            ))
    breakdown["repo_diversity"] = div_pts

    # 6. Description quality (10 pts) ------------------------------------------
    repos_missing_desc = [r for r in repos if not r.get("description")]
    if repos_missing_desc:
        pct = len(repos_missing_desc) / max(len(repos), 1)
        desc_pts = max(0, int(10 * (1 - pct)))
        severity = "high" if pct > 0.5 else "medium"
        findings.append(Finding(
            "description_quality", severity,
            f"{len(repos_missing_desc)}/{len(repos)} repos missing descriptions",
            "GitHub search indexes repo descriptions as keyword signal.",
            "Add a 1-sentence description to every public repo - takes 30 seconds each.",
        ))
    else:
        desc_pts = 10
        findings.append(Finding(
            "description_quality", "good",
            "All repos have descriptions",
            "Every repo is searchable and discoverable by description keyword.",
        ))
    breakdown["description_quality"] = desc_pts

    # 7. Topic tags (5 pts) ----------------------------------------------------
    repos_without_topics = [r for r in repos if not r.get("topics")]
    if not repos_without_topics:
        topic_pts = 5
        findings.append(Finding(
            "topic_tags", "good",
            "All repos have topic tags",
            "Topic tags make repos discoverable via GitHub Explore.",
        ))
    elif len(repos_without_topics) < len(repos) / 2:
        topic_pts = 3
        findings.append(Finding(
            "topic_tags", "low",
            f"{len(repos_without_topics)} repos missing topic tags",
            "GitHub Explore uses topics to surface repos in category feeds.",
            "Add 3-5 relevant topics per repo (e.g. python, cli, api, automation).",
        ))
    else:
        topic_pts = 0
        findings.append(Finding(
            "topic_tags", "medium",
            "Most repos have no topic tags",
            "Missing from GitHub Explore category pages entirely.",
            "Add topics to your top 3 repos today - GitHub UI, takes 2 minutes.",
        ))
    breakdown["topic_tags"] = topic_pts

    # 8. Fork ratio (5 pts) ----------------------------------------------------
    # Reuse the single include_forks fetch from the top of analyze() — no 2nd API call.
    fork_count = sum(1 for r in all_repos if r.get("fork"))
    total_count = len(all_repos)
    fork_ratio = fork_count / total_count if total_count > 0 else 0
    if fork_ratio > 0.7:
        fork_pts = 1
        findings.append(Finding(
            "fork_ratio", "medium",
            f"High fork ratio ({fork_ratio:.0%} forks)",
            "Forked repos dominate your profile. Visitors see mostly borrowed code.",
            "Consider making forked experiments private, or shipping more originals.",
        ))
    elif fork_ratio > 0.4:
        fork_pts = 3
    else:
        fork_pts = 5
    breakdown["fork_ratio"] = fork_pts

    # 9. Recent activity quality (10 pts) --------------------------------------
    recently_active = [
        r for r in repos
        if _days_since(r.get("pushed_at")) is not None
        and (_days_since(r.get("pushed_at")) or 999) < 90
    ]
    if not recently_active:
        ra_pts = 0
        findings.append(Finding(
            "recent_activity", "medium",
            "No repos active in last 90 days",
            "Consistent activity matters for GitHub algorithm visibility.",
            "Even docs or test additions count as activity.",
        ))
    elif len(recently_active) < 2:
        ra_pts = 5
        findings.append(Finding(
            "recent_activity", "low",
            "Only 1 repo active in last 90 days",
            "Single-repo focus is fine but spread to 2-3 for visibility.",
            "Even docs or test additions count.",
        ))
    else:
        ra_pts = 10
        findings.append(Finding(
            "recent_activity", "good",
            f"{len(recently_active)} repos active in last 90 days",
            "Consistent multi-repo activity signals a serious builder.",
        ))
    breakdown["recent_activity"] = ra_pts

    # 10. Release cadence (5 pts) -- NEW ---------------------------------------
    # Published releases signal versioned, production-ready software that
    # users can subscribe to and depend on.
    release_pts = 0
    total_releases = 0
    for repo in top_repos[:5]:
        try:
            releases = client.get(f"/repos/{username}/{repo['name']}/releases",
                                  params={"per_page": 5})
            total_releases += len(releases)
        except Exception:
            pass
    if total_releases == 0:
        release_pts = 0
        if top_repos:
            findings.append(Finding(
                "release_cadence", "low",
                "No published releases",
                "GitHub Releases make your project feel production-ready and "
                "let users subscribe to new versions.",
                "Tag your first release: git tag v0.1.0 && git push --tags, "
                "then create a GitHub release with changelog notes.",
            ))
    elif total_releases < 3:
        release_pts = 3
        findings.append(Finding(
            "release_cadence", "low",
            f"Only {total_releases} published release(s)",
            "A release cadence signals active maintenance.",
            "Aim for a release whenever you ship a meaningful change.",
        ))
    else:
        release_pts = 5
        findings.append(Finding(
            "release_cadence", "good",
            f"{total_releases} published releases across top repos",
            "Regular releases signal a maintained, production-quality project.",
        ))
    breakdown["release_cadence"] = release_pts

    # 11. Profile README signal (5 pts) -- NEW ---------------------------------
    # A profile README (special repo username/username) is displayed at the
    # top of the GitHub profile page - the highest-visibility real estate.
    profile_readme_pts = 0
    try:
        raw = client.get(f"/repos/{username}/{username}/readme")
        profile_text = base64.b64decode(raw["content"]).decode("utf-8", errors="replace")
        word_count = len(profile_text.split())
        if word_count >= 100:
            profile_readme_pts = 5
            findings.append(Finding(
                "profile_readme", "good",
                f"Profile README exists and is substantial ({word_count} words)",
                "A profile README is the highest-visibility real estate on GitHub.",
            ))
        else:
            profile_readme_pts = 2
            findings.append(Finding(
                "profile_readme", "low",
                f"Profile README is short ({word_count} words)",
                "You have a profile README but it could work harder for you.",
                "Add your current focus, top project links, and how to contact you.",
            ))
    except Exception:
        profile_readme_pts = 0
        findings.append(Finding(
            "profile_readme", "medium",
            "No profile README",
            f"A profile README (create repo: {username}/{username}) is the first "
            "thing visitors see. Prime real estate for your personal brand.",
            f"Create a repo named exactly '{username}' with a README.md showing "
            "your focus, skills, and top projects.",
        ))
    breakdown["profile_readme"] = profile_readme_pts

    # Aggregate ----------------------------------------------------------------
    total = sum(breakdown.values())
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "good": 4}
    findings.sort(key=lambda f: severity_order.get(f.severity, 5))

    return ProfileScore(
        username=username,
        total=total,
        breakdown=breakdown,
        findings=findings,
        raw_user=user,
        raw_repos=repos,
    )
