"""Test-case tracker: file-based, tracker-agnostic case storage and reporting."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

VALID_STATUSES = {"untested", "pass", "fail", "blocked"}


def _cases_path(ticket_key: str, base_dir: Path) -> Path:
    return base_dir / ticket_key / "cases.yaml"


def _report_path(ticket_key: str, base_dir: Path) -> Path:
    return base_dir / ticket_key / "report.md"


def create_cases(ticket_key: str, cases: list[dict[str, Any]], base_dir: Path) -> Path:
    """Write the initial case file for a ticket. Each case starts 'untested'."""
    path = _cases_path(ticket_key, base_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    record = [
        {
            "id": case["id"],
            "title": case["title"],
            "steps": case["steps"],
            "expected": case["expected"],
            "status": "untested",
            "verified_via": None,
            "evidence": None,
            "notes": None,
        }
        for case in cases
    ]

    path.write_text(yaml.safe_dump({"ticket": ticket_key, "cases": record}, sort_keys=False))
    return path


def record_result(
    ticket_key: str,
    case_id: str,
    status: str,
    verified_via: str,
    evidence: str,
    base_dir: Path,
    notes: str | None = None,
) -> Path:
    """Update one case's result in place. Raises if the status, case, or file is invalid/missing."""
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}, got {status!r}")

    path = _cases_path(ticket_key, base_dir)
    if not path.exists():
        raise FileNotFoundError(f"no case file for {ticket_key} at {path}")

    data = yaml.safe_load(path.read_text())
    for case in data["cases"]:
        if case["id"] == case_id:
            case["status"] = status
            case["verified_via"] = verified_via
            case["evidence"] = evidence
            if notes is not None:
                case["notes"] = notes
            break
    else:
        raise KeyError(f"no case {case_id!r} in {ticket_key}")

    path.write_text(yaml.safe_dump(data, sort_keys=False))
    return path


def generate_report(ticket_key: str, base_dir: Path) -> Path:
    """Render cases.yaml into a markdown report.md next to it."""
    cases_path = _cases_path(ticket_key, base_dir)
    if not cases_path.exists():
        raise FileNotFoundError(f"no case file for {ticket_key} at {cases_path}")

    data = yaml.safe_load(cases_path.read_text())
    cases = data["cases"]

    lines = [
        f"# Verification report — {ticket_key}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "| Case | Status | Verified via | Evidence |",
        "|---|---|---|---|",
    ]
    for case in cases:
        lines.append(
            f"| {case['id']}: {case['title']} | {case['status']} | "
            f"{case['verified_via'] or '-'} | {case['evidence'] or '-'} |"
        )

    passed = sum(1 for c in cases if c["status"] == "pass")
    failed = sum(1 for c in cases if c["status"] == "fail")
    blocked = sum(1 for c in cases if c["status"] == "blocked")
    untested = sum(1 for c in cases if c["status"] == "untested")
    lines += ["", f"**Summary:** {passed} passed, {failed} failed, {blocked} blocked, {untested} untested."]

    report_path = _report_path(ticket_key, base_dir)
    report_path.write_text("\n".join(lines) + "\n")
    return report_path


def _main() -> None:
    parser = argparse.ArgumentParser(description="File-based test-case tracker")
    parser.add_argument("--base-dir", default="verification-records")
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create")
    p_create.add_argument("ticket_key")
    p_create.add_argument("--cases-json", required=True)

    p_record = sub.add_parser("record")
    p_record.add_argument("ticket_key")
    p_record.add_argument("--case-id", required=True)
    p_record.add_argument("--status", required=True)
    p_record.add_argument("--verified-via", required=True)
    p_record.add_argument("--evidence", required=True)
    p_record.add_argument("--notes", default=None)

    p_report = sub.add_parser("report")
    p_report.add_argument("ticket_key")

    args = parser.parse_args()
    base_dir = Path(args.base_dir)

    if args.command == "create":
        cases = json.loads(Path(args.cases_json).read_text())
        path = create_cases(args.ticket_key, cases, base_dir)
        print(f"wrote {path}")
    elif args.command == "record":
        path = record_result(
            args.ticket_key, args.case_id, args.status, args.verified_via,
            args.evidence, base_dir, args.notes,
        )
        print(f"updated {path}")
    elif args.command == "report":
        path = generate_report(args.ticket_key, base_dir)
        print(f"wrote {path}")


if __name__ == "__main__":
    _main()
