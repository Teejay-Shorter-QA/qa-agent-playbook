import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import generate_summary  # noqa: E402


def test_render_markdown_includes_generated_warning_and_rows():
    rows = [{"component": "example-widget", "owner": "Team Rocket", "contact_channel": "#team-rocket"}]

    output = generate_summary.render_markdown(rows)

    assert "GENERATED FILE — do not hand-edit" in output
    assert "| example-widget | Team Rocket | #team-rocket |" in output


def test_main_writes_summary_from_csv(tmp_path, monkeypatch):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("component,owner,contact_channel\nfoo,Bar Team,#bar\n")
    output_path = tmp_path / "SUMMARY.md"

    monkeypatch.setattr(generate_summary, "CSV_PATH", csv_path)
    monkeypatch.setattr(generate_summary, "OUTPUT_PATH", output_path)

    generate_summary.main()

    assert output_path.exists()
    assert "| foo | Bar Team | #bar |" in output_path.read_text()
