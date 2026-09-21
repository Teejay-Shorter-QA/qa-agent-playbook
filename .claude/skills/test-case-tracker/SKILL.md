---
name: test-case-tracker
description: Use to create, update, and report on file-based test cases for a ticket — the tracker-agnostic baseline for verify-ticket. Owns verification-records/<KEY>/cases.yaml and report.md via scripts/tracker.py. Never hand-edit cases.yaml directly; always go through tracker.py so status transitions stay consistent.
---

# Test Case Tracker (file-based baseline)

Owns case storage and reporting for one ticket at a time: `verification-records/<KEY>/cases.yaml`
(source of truth) and `verification-records/<KEY>/report.md` (generated — don't hand-edit).

## Mechanics

All reads/writes go through `scripts/tracker.py` (requires `PyYAML` — `pip install -r
scripts/requirements.txt`), never hand-edited directly, so status transitions and the case schema
stay consistent no matter which skill is calling in.

```bash
# Create the initial case file (cases start "untested")
python3 scripts/tracker.py create <KEY> --cases-json <path-to-json-list>

# Record one case's result
python3 scripts/tracker.py record <KEY> --case-id <id> --status <pass|fail|blocked> \
  --verified-via <browser|api|cli> --evidence "<one line>" [--notes "<optional>"]

# Regenerate the report from the current case file
python3 scripts/tracker.py report <KEY>
```

Each JSON case object for `create` needs `id`, `title`, `steps` (list of strings), `expected`.

## Case schema (cases.yaml)

```yaml
ticket: <KEY>
cases:
  - id: AC1
    title: <one line>
    steps: [<action>, ...]
    expected: <observable outcome>
    status: untested | pass | fail | blocked
    verified_via: browser | api | cli | null
    evidence: <one line> | null
    notes: <optional> | null
```

## Extension point: a real tracker

See `docs/extension-points.md`. In short: `create_cases`, `record_result`, and `generate_report` in
`scripts/tracker.py` are the entire seam — replace their bodies with API calls to
Testmo/Xray/Zephyr/etc., keep the same function signatures, and nothing calling into this skill
needs to change.

## Error handling

- `record`/`report` against a ticket with no `cases.yaml` yet → raises `FileNotFoundError`; run
  `create` first.
- `record` with an unknown `--case-id` → raises `KeyError`; check the id against `cases.yaml`.
- `record` with a `--status` outside `pass|fail|blocked|untested` → raises `ValueError` before
  writing anything.

## Validation

See `scripts/tests/test_tracker.py` — covers create/record/report and the three error paths, plus
one CLI round-trip test. Run: `python3 -m pytest scripts/tests/`.
