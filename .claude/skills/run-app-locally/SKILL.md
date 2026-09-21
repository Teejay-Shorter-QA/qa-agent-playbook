---
name: run-app-locally
description: Use to bring up a target application locally when no team-specific run skill exists yet. Triggers include "run this app locally", "start <repo> so I can test it", or as Phase 3 of verify-ticket. Discovers the run command from the repo itself rather than assuming a specific stack.
---

# Run App Locally (generic discovery)

Bring up a target repo locally by discovering its own documented run command — never assume a
specific framework.

## Inputs

1. **Repo path** (required).

## Discovery order

Check each in turn, stop at the first match:

1. `Justfile` — look for a `run` (or similarly named) recipe.
2. `Makefile` — look for a `run`/`start`/`dev` target.
3. `README.md` / `README` — look for a fenced code block under a "Running" / "Getting started" /
   "Usage" heading.
4. `docker-compose.yml` / `docker-compose.yaml` — `docker compose up`.
5. None found → **ask the user** for the run command rather than guessing.

## Steps

1. Run discovery in the order above.
2. **Show the derived run plan before executing anything** — the exact command you're about to run
   and where you found it (which file, which section).
3. On confirmation, run it and confirm the app is reachable (a successful health-check request, a
   "listening on" log line, or — for a plain CLI tool with no server — that the binary/script runs
   without error on a no-op-ish invocation).
4. Report how to reach it (URL, or the exact invocation pattern) for the verification phase.

## Known-repo recipes

None shipped in the baseline template — add your own team's known repos here as they come up, the
same way a project-specific run skill can be layered on top of this generic discovery pattern.

## Error handling

- Discovery finds nothing → ask for the run command, don't guess.
- The derived command fails → show the actual error output, don't retry blindly.

## Validation

Run against `fixtures/sample-app/` — discovery should find its `Justfile`'s `run` recipe and confirm
`just run --name Ada --count 1` runs without error.
