#!/usr/bin/env python3
"""Toy CLI fixture for verify-ticket dry runs. Contains one deliberate bug (see SAMPLE-TICKET.md)."""
import argparse


def build_greeting(name: str) -> str:
    return f"Hello, {name}!"


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a greeting some number of times.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    greeting = build_greeting(args.name)
    for _ in range(1):  # BUG: ignores --count, always prints once (see SAMPLE-101 AC1)
        print(greeting)


if __name__ == "__main__":
    main()
