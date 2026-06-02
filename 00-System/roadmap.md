# Reputation Roadmap — The Long Journey

**Owner:** Basil Al Shukaili (@basilalshukaili)
**Goal:** Build genuine, durable GitHub reputation and an engaged audience — culminating in
launching our own successful open-source project(s).
**Method:** Autonomous AI agent (Hermes / Claude Code), quality-first, one project at a time,
honest signals only, reporting to Telegram.

> Grounded in research: GitHub Community Discussion #170732 (followers/stars), dblock's
> "How to Grow Open-Source Contributors and Maintainers" (maintainer trust + meritocracy),
> and the Carnegie Mellon fake-stars study (why we NEVER buy/fake signals).

---

## The Reputation Thesis (what actually works)

Reputation is **earned trust made visible**. It compounds through three flywheels:

1. **Contribution flywheel** — high-quality, tested PRs that maintainers happily merge → you
   become a recognized name in that project → invited to review/triage → promoted toward
   maintainer. (dblock: contributors who write tests + never create technical debt get promoted.)
2. **Audience flywheel** — visible contributions + written content (blog/Dev.to/X about real work)
   → profile views → followers who genuinely engage → amplification of future work.
3. **Creation flywheel** — once trusted and visible, launch our own focused tool that solves a real
   problem → the audience + contribution network gives it its first honest stars and users.

**Hard rule:** Only honest signals. No bought stars, no fake engagement, no AI-slop PR spam.
Detected fakery permanently destroys reputation (CMU study). Slow real trust > fast fake numbers.

---

## What maintainers reward (so we always clear the bar)

From dblock's proven recipe — we mirror these as contributor behaviors:
- PRs solve a real, scoped problem and **include tests + docs**.
- Zero technical debt created; "never make more work for the maintainer."
- Match project conventions exactly; respond to review within hours, graciously.
- Sweat the small stuff. People respond well to high quality standards.
- Engage on issues helpfully (sometimes the best move is a great bug report + failing test).

---

## Phases

### Phase 0 — Foundation  ✅ (done / ongoing)
- System built: second brain repo, model ladder, guardrails, cron cadence, Telegram reporting.
- Profile storefront set up (see Phase 1 — do this first; it's the cheapest reputation win).

### Phase 1 — Profile as Storefront  (week 1)
The profile is what every maintainer/visitor sees. Make it credible BEFORE heavy contributing.
- [ ] Profile README repo (`basilalshukaili/basilalshukaili`): clear bio, what Basil works on,
      focus areas, links. Professional, not cringe.
- [ ] Photo/avatar + bio + location/links filled in.
- [ ] Pin 6 best repos (curate; quality over quantity). Initially: the reputation-engine (if made
      public later) + any real projects.
- [ ] Decide the **niche** — research says focus on 1-2 skills. Candidate: AI agents / developer
      tooling / Python (aligns with the Hermes work). Lock this in `01-Targets/niche.md`.

### Phase 2 — Establish Credibility via Contributions  (weeks 1-6)
Target #1: **NousResearch/hermes-agent** (deep familiarity, dogfooding, Windows niche).
- [ ] Land first merged PR (tested, scoped, conventions-matched).
- [ ] Build to 3-5 merged PRs of increasing substance (bug → test coverage → small feature).
- [ ] Become a recognized contributor: helpful issue comments, review others' PRs where useful.
- [ ] Each merged PR → short journal + (Phase 4) a content post.
- Exit criteria: several merged PRs + positive maintainer interaction. THEN consider project #2.

### Phase 3 — Breadth + Depth  (months 2-4)
- [ ] Expand to 2-3 major projects in the niche (research-selected; one at a time, go deep).
- [ ] Take on meatier issues (features, refactors) where trust is established.
- [ ] Start reviewing others' PRs in projects we know — reviewing is a strong reputation signal.
- [ ] Aim for a "Contributor" acknowledgment / mention / triage rights somewhere.

### Phase 4 — Audience Engine  (runs parallel from Phase 2)
Contributions alone build maintainer trust; CONTENT builds public following.
- [ ] Set up a writing outlet (Dev.to and/or a GitHub Pages blog).
- [ ] After each meaningful PR/learning, publish a short, genuine technical post ("how I fixed X
      in <project>", "what I learned about <topic>"). Link from profile.
- [ ] Cross-post selectively to X/LinkedIn with a visual. No spam — only where relevant.
- [ ] Engage authentically in 1-2 communities (project Discords, relevant subreddits).
- Metric: followers who engage, not vanity counts.

### Phase 5 — Launch Our Own Project  (month 4+)
The payoff. Only attempt once Phases 2-4 have built trust + a small audience.
- [ ] Identify a real, unmet need we discovered WHILE contributing (the best project ideas come
      from friction we personally hit). Capture candidates in `99-Inbox/project-ideas.md`.
- [ ] Build a small, focused, genuinely useful tool/library. Quality over scope.
- [ ] Ship with the full recipe: stellar README (visuals/GIF, badges, clear install/usage),
      LICENSE, CODE_OF_CONDUCT, CONTRIBUTING, high test coverage, passing CI/CD, CHANGELOG.
- [ ] Add `good first issue` / `help wanted` labels to invite contributors (we become the
      benevolent-dictator owner dblock describes).
- [ ] Launch honestly: share with our real audience + relevant communities. NO bought stars.
- [ ] Maintain it well: respond to issues/PRs within ~24h, regular releases. This is what makes
      contributors stay and the project grow.

---

## Success Metrics (tracked in 03-Journal, reviewed in 06-Dreams)
- **Primary:** merged PRs; positive maintainer feedback; review participation.
- **Audience:** genuine followers, post engagement, profile views.
- **Creation:** our project's honest stars, real users, returning contributors.
- **Health (never gamed):** zero spam/low-effort closures; zero fake signals.

## Anti-Goals (reputation poison)
- Bulk low-effort PRs / AI slop · buying stars or followers · faking activity ·
  project-hopping without depth · arguing with maintainers · creating technical debt ·
  degrading PR/comment quality to save tokens.

## Cadence
- 24/7 contribution missions (every 6h) + nightly AI dreaming (synthesis) → Telegram.
- Weekly (in a dream): review phase progress, adjust the niche/target if evidence warrants.
- See `00-System/architecture.md`, `00-System/guardrails.md`, `00-System/cost-and-failover.md`.
