import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "greet.py"


def run_greet(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True, check=True
    )
    return result.stdout


def test_ac2_default_count_prints_once():
    assert run_greet("--name", "Ada").splitlines() == ["Hello, Ada!"]


def test_ac3_greeting_format_uses_name_verbatim():
    assert run_greet("--name", "Ada").strip() == "Hello, Ada!"


def test_ac1_is_seeded_as_a_known_bug():
    """Documents the deliberate fixture bug: --count is ignored.
    verify-ticket's dry run is expected to catch this and record AC1 as `fail`.
    If this test ever fails, someone accidentally fixed the fixture — see SAMPLE-TICKET.md.
    """
    output = run_greet("--name", "Ada", "--count", "3")
    assert output.splitlines() == ["Hello, Ada!"], (
        "expected the seeded bug (count ignored); got a different output — "
        "check SAMPLE-TICKET.md before 'fixing' this"
    )
