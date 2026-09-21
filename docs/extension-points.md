# Extension Points

Two seams in this template are deliberately left unbuilt because they're specific to whatever your
target application and org actually use. Both are documented here with concrete direction, not just
the idea.

## 1. A real test-case tracker (Testmo, Xray, Zephyr, ...)

`test-case-tracker`'s `scripts/tracker.py` exposes exactly three functions — this is the entire
seam:

| Function | Signature | Replace its body with |
|---|---|---|
| `create_cases` | `(ticket_key: str, cases: list[dict], base_dir: Path) -> Path` | An API call that creates cases in your tracker, keyed to `ticket_key` |
| `record_result` | `(ticket_key: str, case_id: str, status: str, verified_via: str, evidence: str, base_dir: Path, notes: str \| None) -> Path` | An API call that records a result against `case_id` in your tracker |
| `generate_report` | `(ticket_key: str, base_dir: Path) -> Path` | A call that reads results back from your tracker and renders/links a report |

Keep the same signatures — everything that calls into `test-case-tracker` (`jira-to-test-cases`,
`verify-ticket`) only ever calls these three functions and never touches `cases.yaml` directly, so
swapping the backend never requires touching the orchestrating skill.

Field mapping from the baseline schema to a typical tracker:

| Baseline field | Typical tracker equivalent |
|---|---|
| `id` | Case key / case ID |
| `title` | Case title |
| `steps` | Case steps (structured step list, if your tracker supports it) |
| `expected` | Expected result |
| `status` | Result status on a run (map `blocked` to whatever your tracker calls an unreachable case) |
| `verified_via` | A custom field or the run's execution-type metadata, if your tracker has one |
| `evidence` | Result comment/note |

## 2. Feature-flag toggling

If your target app has an environment-forced feature flag (or similar server-side config) that
blocks a test case from reaching its expected state — e.g. a flag stuck `on` everywhere, so the
`off` behaviour never appears in any environment you can reach — this is a Phase 4 concern in
`verify-ticket`.

`verify-ticket/SKILL.md`'s Phase 3 section has an "Extension point: feature-flag toggling"
subsection marking exactly where to add a conditional call to your own toggler skill. Write a skill
that:

- accepts: the flag name, the desired treatment, and enough identity/environment info to target it
  (e.g. a user id and an environment name)
- returns: confirmation the flag is now set, and (ideally) a way to revert it when the case is done

Invoke it conditionally — only for cases whose expected state actually needs it — the same way the
source pattern this template comes from invokes its own org-specific flag-toggling skill.

## What's intentionally not here

Squad/folder-ownership resolution (used in the source pattern to locate a tracker folder) has no
pointer here. It only becomes relevant once you've plugged in a real tracker (seam #1 above) — at
that point, folder/ownership resolution belongs inside whatever adapter you write for that tracker,
not in this baseline.
