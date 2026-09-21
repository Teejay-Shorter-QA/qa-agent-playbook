# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

This repo is a Claude Code configuration template for a QA engineering team. **Replace this
paragraph** with your own: what product/team this configures Claude for, and what's out of scope.

@rules/example-rule.md

---

## Persona & Behavior

**Replace this section** with your own team's persona. The shape worth keeping:

### Identity
State how Claude should be addressed and what role it plays (e.g. "a senior QA engineer
companion for team X").

### Communication style
State how technical to be by default, and how to calibrate for less-technical audiences.

### Pushback & professional judgment
State when Claude should push back on a request (e.g. a design that violates a team standard),
and how: name the concern, explain why, offer an alternative, then defer to the human's final call.

### Definition of done
A checklist for "what does complete work look like" in your domain. Example shape (replace with
your own criteria):
- [ ] The right kind of verification for what's being checked (e.g. unit vs. integration vs. e2e)
- [ ] No hardcoded credentials
- [ ] The change was actually run/verified, not just assumed to work

---

## Working Style

- Read before modifying — check existing patterns before introducing new ones.
- Don't silently skip a check — if you skip one, say why.
- **Onboarding-sync rule:** whenever a skill or command is added, renamed, or removed, update the
  roster in `.claude/commands/onboard.md` in the *same* change.
- **Source-of-truth convention.** Where reference data exists (see `resources/example-source-of-truth/`
  for a worked example), keep one raw source file and a generated human-readable doc from it. Never
  hand-edit the generated file — regenerate it instead.
