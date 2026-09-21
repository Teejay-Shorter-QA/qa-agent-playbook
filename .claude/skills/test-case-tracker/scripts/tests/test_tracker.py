import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import tracker  # noqa: E402


SAMPLE_CASES = [
    {
        "id": "AC1",
        "title": "Greeting repeats N times",
        "steps": ["Run `greet.py --name Ada --count 3`"],
        "expected": "The greeting prints exactly 3 times",
    },
    {
        "id": "AC2",
        "title": "Default count is one",
        "steps": ["Run `greet.py --name Ada`"],
        "expected": "The greeting prints exactly once",
    },
]


def test_create_cases_writes_yaml_with_untested_status(tmp_path):
    path = tracker.create_cases("SAMPLE-101", SAMPLE_CASES, tmp_path)

    assert path == tmp_path / "SAMPLE-101" / "cases.yaml"
    data = yaml.safe_load(path.read_text())
    assert data["ticket"] == "SAMPLE-101"
    assert [c["id"] for c in data["cases"]] == ["AC1", "AC2"]
    assert all(c["status"] == "untested" for c in data["cases"])


def test_record_result_updates_matching_case_only(tmp_path):
    tracker.create_cases("SAMPLE-101", SAMPLE_CASES, tmp_path)

    tracker.record_result(
        "SAMPLE-101", "AC1", "fail", "cli", "printed once instead of 3 times", tmp_path
    )

    data = yaml.safe_load((tmp_path / "SAMPLE-101" / "cases.yaml").read_text())
    ac1, ac2 = data["cases"]
    assert ac1["status"] == "fail"
    assert ac1["verified_via"] == "cli"
    assert ac1["evidence"] == "printed once instead of 3 times"
    assert ac2["status"] == "untested"


def test_record_result_rejects_unknown_status(tmp_path):
    tracker.create_cases("SAMPLE-101", SAMPLE_CASES, tmp_path)

    with pytest.raises(ValueError):
        tracker.record_result("SAMPLE-101", "AC1", "maybe", "cli", "n/a", tmp_path)


def test_record_result_missing_case_raises_key_error(tmp_path):
    tracker.create_cases("SAMPLE-101", SAMPLE_CASES, tmp_path)

    with pytest.raises(KeyError):
        tracker.record_result("SAMPLE-101", "AC99", "pass", "cli", "n/a", tmp_path)


def test_generate_report_renders_table_and_summary(tmp_path):
    tracker.create_cases("SAMPLE-101", SAMPLE_CASES, tmp_path)
    tracker.record_result("SAMPLE-101", "AC1", "fail", "cli", "printed once instead of 3 times", tmp_path)
    tracker.record_result("SAMPLE-101", "AC2", "pass", "cli", "printed once as expected", tmp_path)

    report_path = tracker.generate_report("SAMPLE-101", tmp_path)

    text = report_path.read_text()
    assert "SAMPLE-101" in text
    assert "AC1: Greeting repeats N times" in text
    assert "fail" in text
    assert "1 passed, 1 failed, 0 blocked, 0 untested." in text


def test_cli_create_record_report_round_trip(tmp_path):
    cases_json = tmp_path / "cases_input.json"
    cases_json.write_text(json.dumps(SAMPLE_CASES))
    script = Path(__file__).resolve().parents[1] / "tracker.py"

    subprocess.run(
        [sys.executable, str(script), "--base-dir", str(tmp_path),
         "create", "SAMPLE-101", "--cases-json", str(cases_json)],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(script), "--base-dir", str(tmp_path),
         "record", "SAMPLE-101", "--case-id", "AC1", "--status", "fail",
         "--verified-via", "cli", "--evidence", "printed once instead of 3 times"],
        check=True,
    )
    subprocess.run(
        [sys.executable, str(script), "--base-dir", str(tmp_path), "report", "SAMPLE-101"],
        check=True,
    )

    report = (tmp_path / "SAMPLE-101" / "report.md").read_text()
    assert "fail" in report
