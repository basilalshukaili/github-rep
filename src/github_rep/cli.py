"""CLI entry point for github-rep."""

from __future__ import annotations

import json
import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .analyzer import analyze, ProfileScore
from .api import RateLimitError, GitHubClient

app = typer.Typer(
    name="github-rep",
    help="Analyze a GitHub profile and get honest, actionable reputation advice.",
    add_completion=False,
)
console = Console()


def _severity_color(severity: str) -> str:
    return {
        "critical": "bold red",
        "high":     "red",
        "medium":   "yellow",
        "low":      "blue",
        "good":     "green",
    }.get(severity, "white")


def _grade_color(grade: str) -> str:
    return {"A": "bold green", "B": "green", "C": "yellow", "D": "orange3", "F": "red"}.get(grade, "white")


# Dimension max scores (must stay in sync with analyzer.py)
DIMENSION_MAX = {
    "profile_completeness": 10,
    "readme_quality":       15,
    "star_signal":          20,
    "contribution_streak":  15,
    "repo_diversity":       10,
    "description_quality":  10,
    "topic_tags":            5,
    "fork_ratio":            5,
    "recent_activity":      10,
    "release_cadence":       5,
    "profile_readme":        5,
}


def _render_score(score: ProfileScore, verbose: bool = False) -> None:
    """Render a ProfileScore to the terminal using Rich."""
    grade_color = _grade_color(score.grade)

    user = score.raw_user
    header_lines = [
        f"[bold]@{score.username}[/bold]  |  {user.get('name', '')}",
        f"{user.get('bio', '')}",
        f"Followers: {user.get('followers', 0)}  |  "
        f"Public repos: {user.get('public_repos', 0)}  |  "
        f"Stars earned: {sum(r.get('stargazers_count', 0) for r in score.raw_repos)}",
    ]
    console.print(Panel("\n".join(header_lines), title="GitHub Profile", border_style="blue"))

    grade_text = Text(f"Grade: {score.grade}  ({score.total}/100)", style=grade_color)
    tier_text = Text(f"Tier: {score.tier}", style="bold")
    console.print(grade_text)
    console.print(tier_text)
    console.print()

    table = Table(title="Score Breakdown", show_header=True, header_style="bold cyan")
    table.add_column("Dimension", min_width=24)
    table.add_column("Score", justify="right", min_width=8)
    table.add_column("Max",   justify="right", min_width=5)

    for dim, pts in score.breakdown.items():
        max_pts = DIMENSION_MAX.get(dim, 10)
        label = dim.replace("_", " ").title()
        color = "green" if pts >= max_pts * 0.8 else "yellow" if pts >= max_pts * 0.5 else "red"
        table.add_row(label, f"[{color}]{pts}[/{color}]", str(max_pts))

    console.print(table)
    console.print()

    critical_and_high = [f for f in score.findings if f.severity in ("critical", "high")]
    medium_and_low = [f for f in score.findings if f.severity in ("medium", "low")]
    good = [f for f in score.findings if f.severity == "good"]

    if critical_and_high:
        console.print("[bold red]Priority fixes:[/bold red]")
        for f in critical_and_high:
            color = _severity_color(f.severity)
            console.print(f"  [{color}]{f.icon} {f.title}[/{color}]")
            console.print(f"     {f.detail}")
            if f.fix:
                console.print(f"     [dim]Fix: {f.fix}[/dim]")
        console.print()

    if medium_and_low and (verbose or not critical_and_high):
        console.print("[bold yellow]Improvements:[/bold yellow]")
        for f in medium_and_low:
            color = _severity_color(f.severity)
            console.print(f"  [{color}]{f.icon} {f.title}[/{color}]")
            if verbose:
                console.print(f"     {f.detail}")
                if f.fix:
                    console.print(f"     [dim]Fix: {f.fix}[/dim]")
        console.print()

    if good:
        console.print("[bold green]What is working:[/bold green]")
        for f in good:
            console.print(f"  [green]{f.icon} {f.title}[/green]")
            if verbose:
                console.print(f"     [dim]{f.detail}[/dim]")
        console.print()


# -- Commands ------------------------------------------------------------------

@app.command()
def analyze_profile(
    username: str = typer.Argument(..., help="GitHub username to analyze"),
    token: Optional[str] = typer.Option(
        None, "--token", "-t", envvar="GITHUB_TOKEN",
        help="GitHub personal access token (optional; raises rate limit to 5000 req/hr)",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show all findings including low-priority"),
    json_output: bool = typer.Option(False, "--json", help="Output results as JSON"),
    top_n: int = typer.Option(10, "--top", help="Number of top repos to deep-analyze"),
) -> None:
    """Analyze a GitHub profile and score it across 11 genuine reputation dimensions.

    Examples:
        github-rep analyze-profile torvalds
        github-rep analyze-profile basilalshukaili --verbose
        github-rep analyze-profile sindresorhus --json
        GITHUB_TOKEN=ghp_xxx github-rep analyze-profile gvanrossum
    """
    try:
        with console.status(f"[cyan]Analyzing @{username}...[/cyan]", spinner="dots"):
            score = analyze(username, token=token, top_n=top_n)
    except RateLimitError as e:
        console.print(f"[red]Rate limit hit:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error analyzing @{username}:[/red] {e}")
        raise typer.Exit(1)

    if json_output:
        output = {
            "username": score.username,
            "total": score.total,
            "grade": score.grade,
            "tier": score.tier,
            "breakdown": score.breakdown,
            "findings": [
                {
                    "category": f.category,
                    "severity": f.severity,
                    "title": f.title,
                    "detail": f.detail,
                    "fix": f.fix,
                }
                for f in score.findings
            ],
        }
        print(json.dumps(output, indent=2))
        return

    _render_score(score, verbose=verbose)


@app.command()
def compare(
    usernames: list[str] = typer.Argument(..., help="Two or more GitHub usernames to compare"),
    token: Optional[str] = typer.Option(None, "--token", "-t", envvar="GITHUB_TOKEN"),
) -> None:
    """Compare two or more GitHub profiles side by side.

    Example:
        github-rep compare torvalds gvanrossum sindresorhus
    """
    if len(usernames) < 2:
        console.print("[red]Provide at least 2 usernames to compare.[/red]")
        raise typer.Exit(1)

    scores = []
    for username in usernames:
        try:
            with console.status(f"[cyan]Analyzing @{username}...[/cyan]", spinner="dots"):
                scores.append(analyze(username, token=token))
        except Exception as e:
            console.print(f"[yellow]Skipping @{username}: {e}[/yellow]")

    if not scores:
        raise typer.Exit(1)

    table = Table(title="Profile Comparison", show_header=True, header_style="bold cyan")
    table.add_column("Dimension", min_width=24)
    for s in scores:
        table.add_column(f"@{s.username}", justify="right", min_width=12)

    dimensions = list(DIMENSION_MAX.keys())
    for dim in dimensions:
        row = [dim.replace("_", " ").title()]
        for s in scores:
            pts = s.breakdown.get(dim, 0)
            row.append(str(pts))
        table.add_row(*row)

    totals = ["[bold]TOTAL[/bold]"]
    for s in scores:
        grade_color = _grade_color(s.grade)
        totals.append(f"[{grade_color}]{s.total} ({s.grade})[/{grade_color}]")
    table.add_row(*totals)

    console.print(table)


@app.command()
def rate_limit(
    token: Optional[str] = typer.Option(None, "--token", "-t", envvar="GITHUB_TOKEN"),
) -> None:
    """Check your current GitHub API rate limit status."""
    client = GitHubClient(token=token)
    try:
        data = client.rate_limit_status()
        core = data.get("resources", {}).get("core", {})
        remaining = core.get("remaining", "?")
        limit = core.get("limit", "?")
        reset_ts = core.get("reset")
        import time
        reset_str = time.ctime(reset_ts) if reset_ts else "?"
        console.print(f"[cyan]Rate limit:[/cyan] {remaining}/{limit} remaining, resets at {reset_str}")
        if not token:
            console.print("[yellow]Tip: set GITHUB_TOKEN to get 5000 req/hr instead of 60.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
