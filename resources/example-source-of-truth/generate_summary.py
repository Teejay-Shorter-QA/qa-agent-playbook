"""Regenerate SUMMARY.md from data.csv. Never hand-edit SUMMARY.md — run this instead."""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).parent
CSV_PATH = HERE / "data.csv"
OUTPUT_PATH = HERE / "SUMMARY.md"


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="") as f:
        return list(csv.DictReader(f))


def render_markdown(rows: list[dict[str, str]]) -> str:
    lines = [
        "<!-- GENERATED FILE — do not hand-edit. Regenerate with: python generate_summary.py -->",
        "",
        "# Component ownership",
        "",
        "| Component | Owner | Contact |",
        "|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['component']} | {row['owner']} | {row['contact_channel']} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    rows = load_rows(CSV_PATH)
    OUTPUT_PATH.write_text(render_markdown(rows))
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
