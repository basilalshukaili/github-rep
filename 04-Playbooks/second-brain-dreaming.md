# Playbook: Second Brain & AI Dreaming

This repo is plain Markdown — any agent edits it with normal file tools. Obsidian `[[wikilinks]]`
connect notes (and render as a graph in the Obsidian app).

## Journaling (after every mission)

Append to today's `03-Journal/YYYY-MM-DD.md`:
- What was attempted, on which repo/issue (link).
- What the Worker model did vs what the Brain did/redid.
- PRs opened/updated/merged (links + status).
- Blockers, decisions, token notes.
- Link relevant `[[02-Repos/...]]` and `[[05-Lessons/...]]`.

## Lessons (capture immediately when learned)

In `05-Lessons/`, one file per durable lesson. Format: situation → what went wrong/right → rule
for next time. If procedural, ALSO update the relevant playbook.

## AI Dreaming (nightly)

"Dreaming" = stepping back from execution to synthesize and connect dots. Write to
`06-Dreams/YYYY-MM-DD.md`:

1. Read the last 1-3 days of `03-Journal/`, current `05-Lessons/`, and `01-Targets/current.md`.
2. Reflect:
   - **Patterns:** what's working? what keeps going wrong? repeated worker failure modes?
   - **Connections:** link insights across repos/lessons with `[[wikilinks]]`. New angles?
   - **Reputation read:** how is the current project relationship developing? next best move?
   - **Self-improvement:** which playbook should change? propose concrete edits.
   - **Tomorrow's plan:** the single most valuable next action.
3. If the reflection yields a concrete process improvement, update the relevant playbook NOW.
4. Update `01-Targets/current.md` if strategy shifts (but don't project-hop without exhausting
   the current target).
5. Post a short dream digest to Telegram (3-5 lines: insight + tomorrow's plan).

Dreaming is where the system gets smarter. Be honest about failures — that's the point.

## Pitfalls

- Keep journals append-only for the day; don't overwrite earlier entries.
- Dreams are for synthesis, not re-logging — add insight, don't repeat the journal.
- On Windows + git-bash, write files with native `C:\...` paths, not `/c/...`.
