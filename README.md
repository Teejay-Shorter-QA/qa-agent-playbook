# QA Agent Playbook

A reusable Claude Code configuration template for QA engineering teams — the rules/skills/commands
architecture pattern, plus one worked end-to-end example: verify a Jira ticket from requirements
gathering through generated test cases, a manual run-through, and recorded results.

This is a **template**, not a finished tool for any specific product. Replace the placeholder
content in `CLAUDE.md` and the example skill/rule with your own team's conventions.

## Contents

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Entry point: identity, tone, Definition of Done, links to `.claude/rules/` |
| `.claude/rules/` | Short, always-loaded constraints |
| `.claude/skills/verify-ticket/` | Flagship end-to-end skill: Jira ticket → cases → run → verify → results/report → comment |
| `.claude/skills/jira-to-test-cases/` | Generates test cases from a ticket's Acceptance Criteria |
| `.claude/skills/run-app-locally/` | Generic local-run discovery (README/Justfile/Makefile/docker-compose) |
| `.claude/skills/test-case-tracker/` | File-based, tracker-agnostic case storage and reporting |
| `.claude/commands/onboard.md` | Guided first-run setup |
| `resources/example-source-of-truth/` | Example of the CSV-source → generated-doc convention |
| `docs/extension-points.md` | Where to plug in a real test-case tracker or feature-flag toggling, if you need either |
| `fixtures/sample-app/` | Toy CLI app + sample ticket, for dry-running `verify-ticket` before pointing it at a real project |

## Setup

```sh
cp .env.example .env
```

Edit `.env` and set `TARGET_APP_DIR` to the absolute path of the product repo you'll be verifying
tickets against.

The test-case tracker script needs its own Python dependencies (PEP 668 "externally-managed-environment"
blocks a bare `pip install` on modern macOS/Debian/Ubuntu, so use a venv):

```sh
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r .claude/skills/test-case-tracker/scripts/requirements.txt
```

To run every automated test in the repo (not just the ones a root-level `pytest` would collect —
see `pytest.ini`):

```sh
python3 -m pytest
```

## Plugins

`.claude/settings.json` ships with an empty permissions skeleton. The setup this template is
generalized from also wires up an organization-internal Claude Code plugin marketplace — that's
deliberately **not** included here, since it wouldn't resolve outside that org. If your org has an
equivalent plugin marketplace, add your own `enabledPlugins` block to
`.claude/settings.json`.

## Try it before you customize it

`fixtures/sample-app/` is a tiny, deliberately-buggy CLI tool with a matching sample ticket. Dry-run
`verify-ticket` against it (see that skill's own Validation section) before pointing this template at
a real project, to confirm the mechanics work in your environment.
