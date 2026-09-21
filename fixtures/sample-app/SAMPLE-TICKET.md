# SAMPLE-101 — Greeting should repeat N times

## Description

`greet.py` should print its greeting `--count` times. Right now it only ever prints once.

## Acceptance Criteria

- AC1: Given `--name Ada --count 3`, running `python3 greet.py --name Ada --count 3` prints
  "Hello, Ada!" exactly three times.
- AC2: Given `--name Ada` with no `--count`, the greeting prints exactly once (the default).
- AC3: The greeting format is exactly `Hello, <name>!` with the name used verbatim as given.
