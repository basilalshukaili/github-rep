# Active Targets (two-front, 2026-07-02)

## Front 1: NousResearch/hermes-agent — 2 MERGED, 1 in flight
**Status:** Graduation criteria met (2-3 merged PRs). Maintain presence, respond to reviews fast.
| Contribution | Status |
|---|---|
| #38832 compression contamination fix | ✅ Merged via #41717 (Jun 8) |
| #43293 tail-budget token undercount | ✅ Merged via `72f75f845` (authorship preserved) |
| #56877 Windows console-flash, GUI exec paths | 🟢 Open — CI 20/20 green, awaiting review |

**Follow-up bench (unclaimed, audited 2026-07-02):** docker.py 17 spawn sites, computer_use/doctor.py, env_probe `_run`, lazy_deps, banner.py git calls, web_git.py, tools_config installers. Ship as scoped PRs only if maintainer signals interest on #56877. Avoid the spam pile (~50 bounty PRs on this bug class; 3 reverted mass sweeps — stay surgical).

## Front 2: langchain-ai/langchain — OPENING (2026-07-02)
**Protocol (hard rule):** bot auto-closes PRs from unassigned contributors. Sequence: substantive diagnosis comment → maintainer assigns → THEN PR.
**Verified-open, unassigned targets (June diagnoses, re-verification in progress):**
| Issue | Bug | Owner |
|---|---|---|
| #37673 | VectorStore.add_texts exhausts generator → 0 docs added (core infra) | Worker A (clone + fix + tests) |
| #37596 | ChatAnthropic.bind_tools mutates caller tool_choice dict | Worker A |
| #37894 | convert_to_openai_messages mutates caller message dict | Worker B (read-only verify) |
| #37761 | _to_protocol_usage drops token_details in v3 streaming | Worker B |
(#37736 closed upstream — dropped.)

**Next actions:** review worker reports → post diagnosis comments under @basilalshukaili → on assignment, push staged branches + open PRs.

## Standing lessons
- Re-verify ALL bench intel against current main before coding — it rots in weeks (#42776, TTL bug, #37736 all died stale).
- One scoped, evidence-backed PR beats any sweep. Honesty about what wasn't verifiable IS the differentiator.
- Identity: basilalshukaili + basilalshukaili@gmail.com, always, every clone.
