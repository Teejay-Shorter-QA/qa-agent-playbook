# /onboard

Guided first-run setup for this QA agent playbook template.

## Step 1 — Environment

```sh
cp .env.example .env
```

Set `TARGET_APP_DIR` in `.env` to the absolute path of the product repo you'll verify tickets
against.

## Step 2 — Install the tracker script's dependencies

```sh
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r .claude/skills/test-case-tracker/scripts/requirements.txt
```

## Step 3 — Try the fixture

Before pointing this at a real project, dry-run `verify-ticket` against `fixtures/sample-app/` and
its `SAMPLE-TICKET.md` (read as a local file in place of a real Jira ticket) to confirm the
mechanics work in your environment: three cases generated, the app runs via `just run`, AC1 comes
back `fail` (it's a seeded bug), AC2/AC3 come back `pass`.

## Step 4 — Customize

Replace the placeholder content in `CLAUDE.md` (identity, tone, Definition of Done) and
`.claude/rules/example-rule.md` with your own team's conventions.

## Roster — keep this in sync

Whenever a skill or command is added, renamed, or removed, update this table in the same change.

| Type | Name | Purpose |
|---|---|---|
| Skill | `verify-ticket` | Flagship end-to-end flow: ticket → cases → run → verify → results/report → comment |
| Skill | `jira-to-test-cases` | Generates test cases from a ticket's Acceptance Criteria |
| Skill | `run-app-locally` | Generic local-run discovery |
| Skill | `test-case-tracker` | File-based case storage, results, and reporting |
| Rule | `example-rule.md` | Demonstrates the rule-file pattern — replace with your own |
| Command | `/onboard` | This guided setup |
