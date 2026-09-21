---
name: jira-to-test-cases
description: Use to generate a structured, file-based test-case list from a Jira ticket's Acceptance Criteria. Triggers include "generate test cases for <KEY>", "turn <KEY>'s AC into test cases", or as Phase 2 of the verify-ticket skill. Writes cases via the test-case-tracker skill's tracker.py — never hand-writes the YAML file directly.
---

# Jira → Test Cases

Turn one Jira ticket's Acceptance Criteria into a structured case list, stored via
`test-case-tracker`.

## Inputs

1. **Jira key** (required), e.g. `SAMPLE-101`.

## Steps

1. Fetch the ticket with the Atlassian MCP `getJiraIssue` tool (`fields: ["*all"]`). Read the
   description and any Acceptance-Criteria-shaped content.
2. **Extract Acceptance Criteria.** Look for a dedicated AC field first; if none, fall back to a
   checklist/bulleted list in the description. Each distinct, independently-verifiable criterion
   becomes one case.
3. For each criterion, build a case object:
   - `id`: a short stable identifier (e.g. `AC1`, `AC2`, ...).
   - `title`: one line describing what's being checked.
   - `steps`: the concrete actions to take to exercise it (a short ordered list).
   - `expected`: the observable outcome that means it passed.
4. Write the cases via `test-case-tracker`: put the case list in a temp JSON file and run
   `python3 <repo>/.claude/skills/test-case-tracker/scripts/tracker.py create <KEY> --cases-json <path>`.
5. Report the case count and the path `verification-records/<KEY>/cases.yaml` back to the user.

## Error handling

- No Acceptance Criteria and no checklist in the description → say so and ask the user to point at
  the right field, don't invent criteria.
- Ticket not found → report the exact key that failed to resolve.

## Validation

Run against `fixtures/sample-app/SAMPLE-TICKET.md`'s three ACs (read as a local file, not a real
Jira ticket, when dry-running without Jira access) and confirm `cases.yaml` has three cases matching
them.
